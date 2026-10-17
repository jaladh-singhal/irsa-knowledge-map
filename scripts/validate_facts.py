#!/usr/bin/env python3
"""Check knowledge-map facts against live IRSA services.

For every `access` entry: TAP/SCS tables and SIA/SSA collections are listed by
astroquery (`Irsa.list_catalogs`, `Irsa.list_collections`), and S3/HATS prefixes
are non-empty. Every URL (overview, docs, tools, tutorials, browse) must respond. URLs disallowed by IRSA's robots.txt are not
fetched: /ibe/data/ paths are checked through their S3 mirror, others are skipped.

A failed check is re-checked once after a pause; it fails only if it fails both times.
Prints failures, warnings and skips; --verbose prints every check. Exits 1 if any
check fails. Writes a Markdown report to $GITHUB_STEP_SUMMARY when set, with every
check in a collapsed section.
"""

import argparse
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from functools import cache
from pathlib import Path
from urllib.robotparser import RobotFileParser

import requests
import s3fs
import yaml
from astroquery.ipac.irsa import Irsa
from pyvo.dal import DALAccessError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import km_lookup  # noqa: E402  (repo-root helper)
IRSA = "https://irsa.ipac.caltech.edu"
TIMEOUT = 60
RECHECK_DELAY = 30  # seconds before re-checking failures

# On-prem IBE tree -> S3 mirror. TODO: drop once CI may query /ibe/data/ (see README).
IBE_TO_S3 = {
    f"{IRSA}/ibe/data/euclid/q1/": "nasa-irsa-euclid-q1/q1/",
    f"{IRSA}/ibe/data/spherex/": "nasa-irsa-spherex/",
}

session = requests.Session()
session.headers["User-Agent"] = "irsa-knowledge-map-validate-facts"
session.mount("https://", HTTPAdapter(max_retries=Retry(
    total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])))

s3 = s3fs.S3FileSystem(anon=True)

robots = RobotFileParser(f"{IRSA}/robots.txt")
robots.read()


# --- individual checks: each returns (status, detail), status in ok | warn | fail | skip

@cache
def tap_tables():
    return {name.lower() for name in Irsa.list_catalogs(include_metadata_tables=True)}


@cache
def collections(servicetype):
    return set(Irsa.list_collections(servicetype=servicetype)["collection"])


def check_tap(table):
    return ("ok", "") if table.lower() in tap_tables() else ("fail", "not in Irsa.list_catalogs()")


def check_sia(collection):
    return ("ok", "") if collection in collections("SIA") else ("fail", "not in Irsa.list_collections('SIA')")


def check_ssa(collection):
    return ("ok", "") if collection in collections("SSA") else ("fail", "not in Irsa.list_collections('SSA')")


def check_s3(path):
    try:
        entries = s3.ls(path.removeprefix("s3://"), refresh=True)
    except FileNotFoundError:
        return "fail", "S3 prefix or bucket not found"
    return ("ok", "") if entries else ("fail", "S3 prefix is empty")


def check_url(url):
    for ibe_root, s3_root in IBE_TO_S3.items():
        if url.startswith(ibe_root):
            status, detail = check_s3(s3_root + url.removeprefix(ibe_root))
            return status, detail or "checked via S3 mirror"
    if url.startswith(f"{IRSA}/ibe/data/"):
        return "warn", "no S3 copy mapped for this /ibe/data/ path; add one to IBE_TO_S3"
    if url.startswith(IRSA) and not robots.can_fetch("*", url):
        return "skip", "disallowed by robots.txt"
    response = session.get(url, timeout=TIMEOUT, stream=True, allow_redirects=True)
    if response.status_code == 404 and url.startswith(f"{IRSA}/applications/"):
        # App deep links: the server sends the app shell with a 404 and the app routes in the browser.
        first_bytes = next(response.iter_content(512), b"").decode(errors="ignore").lower()
        response.close()
        return ("warn", "app route served with HTTP 404") if "<!doctype html" in first_bytes else ("fail", "HTTP 404")
    response.close()
    return ("ok", "") if response.status_code < 400 else ("fail", f"HTTP {response.status_code}")


@cache
def tutorial_index():
    """Every notebook path listed in irsa-tutorials' notebook_metadata.yml."""
    config = km_lookup._read("irsa.yaml", str(ROOT))["tutorials"]
    response = session.get(config["source_prefix"] + config["index"], timeout=TIMEOUT)
    response.raise_for_status()
    return {notebook["file"] for notebook in yaml.safe_load(response.text)}


def check_tutorial_listed(source_path):
    return ("ok", "") if source_path in tutorial_index() else ("fail", "not in irsa-tutorials' notebook_metadata.yml")


ACCESS_CHECKS = {"tap": check_tap, "scs": check_tap, "sia": check_sia, "ssa": check_ssa,
                 "s3": check_s3, "hats": check_s3, "browse": check_url, "moc": check_url}


# --- collect checks from the YAML

def collect():
    checks = []  # (where, what, func, arg)

    def url(where, value):
        if isinstance(value, str) and value.startswith("http"):
            checks.append((where, value, check_url, value))

    for path in sorted((ROOT / "missions").glob("*.yaml")):
        mission = path.stem
        mission_file = km_lookup.load(mission, source=str(ROOT))
        url(f"{mission}: archive_page", mission_file["mission"].get("archive_page"))
        for collection in mission_file.get("collections") or []:
            url(f"{collection['id']}: overview", collection.get("overview"))
            for dataset in collection.get("datasets") or []:
                for doc in dataset.get("docs") or []:
                    url(f"{dataset['id']}: docs", doc)
        for _, dataset, entry in km_lookup.iter_access(mission_file):
            via, name = entry["via"], entry.get("name")
            if via not in ACCESS_CHECKS or not name or entry.get("status") == "planned":
                continue
            if via == "browse" and not str(name).startswith("http"):
                continue  # a bare filename, relative to the overview page
            checks.append((f"{dataset['id']}: {via}", name, ACCESS_CHECKS[via], name))
        for tool in mission_file.get("tools") or []:
            url(f"{mission} tool {tool['name']}: url", tool.get("url"))
            url(f"{mission} tool {tool['name']}: docs", tool.get("docs"))
        for issue in mission_file.get("known_issues") or []:
            url(f"{mission} known issue {issue['title']}: link", issue.get("link"))
        for tutorial in km_lookup.tutorials(mission_file):
            url(f"{mission} tutorial: url", tutorial.get("url"))
            url(f"{mission} tutorial: source", tutorial["source_url"])
            checks.append((f"{mission} tutorial: listed", tutorial["source"], check_tutorial_listed, tutorial["source"]))
        for doc in mission_file.get("docs") or []:
            url(f"{mission} doc {doc['title']}: url", doc.get("url"))

    for key, service in km_lookup.services(source=str(ROOT)).items():
        url(f"irsa service {key}: docs", service.get("docs"))
    return checks


def check_product_keys():
    """Every dataset's product key must be declared in its mission's `products` list."""
    results = []
    for path in sorted((ROOT / "missions").glob("*.yaml")):
        mission_file = km_lookup.load(path.stem, source=str(ROOT))
        declared = km_lookup.products(mission_file)
        for collection in mission_file.get("collections") or []:
            for dataset in collection.get("datasets") or []:
                key = dataset["id"].split(".", 2)[-1]
                status, detail = ("ok", "") if key in declared else ("fail", "product key not declared in `products`")
                results.append((f"{dataset['id']}: product key", key, status, detail))
    return results


def run(check):
    where, what, func, arg = check
    try:
        status, detail = func(arg)
    except (requests.RequestException, DALAccessError, OSError) as error:
        status, detail = "fail", f"{type(error).__name__}: {error}"[:200]
    return where, what, status, detail


def table(results):
    rows = ["| Result | Where | Checked | Detail |", "|---|---|---|---|"]
    return rows + [f"| {status} | {where} | `{what}` | {detail} |" for where, what, status, detail in results]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-v", "--verbose", action="store_true", help="print every check, including ok ones")
    args = parser.parse_args(argv)

    checks = collect()
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(run, checks))

        # Re-check failures once after a pause, so a brief network glitch doesn't fail the run.
        failed = [i for i, result in enumerate(results) if result[2] == "fail"]
        if failed:
            print(f"{len(failed)} failed; re-checking in {RECHECK_DELAY} s")
            time.sleep(RECHECK_DELAY)
            for i, recheck in zip(failed, pool.map(run, [checks[i] for i in failed])):
                where, what, status, detail = recheck
                if status != "fail":
                    status, detail = "warn", f"passed on re-check; first try: {results[i][3]}"
                results[i] = (where, what, status, detail)

    results = check_product_keys() + results   # structural, no network: never re-checked

    by_status = {status: [result for result in results if result[2] == status]
                 for status in ("ok", "warn", "fail", "skip")}
    counts = ", ".join(f"{len(found)} {status}" for status, found in by_status.items())
    listed = by_status["fail"] + by_status["warn"] + by_status["skip"]

    for where, what, status, detail in results if args.verbose else listed:
        print(f"{status.upper():5} {where}  {what}" + (f"  ({detail})" if detail else ""))
    print(f"\n{counts} ({len(results)} total)")

    if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
        lines = [f"## Validate facts against IRSA: {counts}\n"]
        if listed:
            lines += table(listed) + [""]
        lines += ["<details><summary>Show all checks</summary>\n"] + table(results) + ["\n</details>"]
        Path(summary).write_text("\n".join(lines) + "\n")

    sys.exit(1 if by_status["fail"] else 0)


if __name__ == "__main__":
    main()
