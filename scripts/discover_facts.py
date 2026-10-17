#!/usr/bin/env python3
"""Find IRSA collections, tables and S3 prefixes that the knowledge map doesn't list yet.

Compares what IRSA lists live (SIA/SSA collections and TAP tables via astroquery, the first
two levels of prefixes in each mission's S3 buckets, and notebooks in the mission's section of
irsa-tutorials' notebook_metadata.yml) against the `access` entries in the mission files.
A live item counts as known only if the same service lists it (e.g. `via: sia`), and a
collection or table belongs to a mission when its name contains the mission id.

Prints a Markdown report with a ready-to-paste YAML line per new item, and writes it to
--output if given. Exit code is 0 whether or not anything new is found.
"""

import argparse
import sys
import re
from datetime import date
from urllib.request import urlopen
from pathlib import Path

import s3fs
import yaml
from astroquery.ipac.irsa import Irsa

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import km_lookup  # noqa: E402  (repo-root helper)


def load_missions():
    """Map mission id -> (known (via, name) pairs, known S3 paths like "bucket/q1/MER/")."""
    missions = {}
    for path in sorted((ROOT / "missions").glob("*.yaml")):
        known, s3_paths = set(), set()
        for _, _, entry in km_lookup.iter_access(km_lookup.load(path.stem, source=str(ROOT))):
            name = str(entry.get("name") or "")
            known.add((entry["via"], name.lower()))
            if entry["via"] in ("s3", "hats"):
                s3_paths.add(name.removeprefix("s3://").rstrip("/") + "/")
        missions[path.stem] = (known, s3_paths)
    return missions


def s3_directories(path):
    """Subdirectories of an S3 path, e.g. "bucket/" -> ["bucket/qr2/", "bucket/qr3/"] (files excluded)."""
    entries = s3fs.S3FileSystem(anon=True).ls(path, detail=True, refresh=True)
    return [entry["name"] + "/" for entry in entries if entry["type"] == "directory"]


def is_covered(path, s3_paths):
    """A live S3 directory is covered if a known path lies inside it or contains it."""
    return any(known.startswith(path) or path.startswith(known) for known in s3_paths)


def tutorial_notebooks():
    """Notebooks listed in irsa-tutorials' notebook_metadata.yml: [{title, file, section, ...}]."""
    config = km_lookup._read("irsa.yaml", str(ROOT))["tutorials"]
    with urlopen(config["source_prefix"] + config["index"]) as response:
        return yaml.safe_load(response.read())


def page_url(file):
    """Published page of a notebook: file name without its number prefix, lower-cased, _ -> -."""
    stem = file.rsplit("/", 1)[-1].removesuffix(".md")
    return "https://caltech-ipac.github.io/irsa-tutorials/" + re.sub(r"^\d+[-_]", "", stem).lower().replace("_", "-") + "/"


def discover():
    """Return {mission id: [YAML stub lines for items not in the knowledge map]}."""
    live = {
        "sia": {name: "SIA collection" for name in Irsa.list_collections(servicetype="SIA")["collection"]},
        "ssa": {name: "SSA collection" for name in Irsa.list_collections(servicetype="SSA")["collection"]},
        "tap": Irsa.list_catalogs(include_metadata_tables=True),  # table name -> description
    }
    notebooks = tutorial_notebooks()
    report = {}
    for mission, (known, s3_paths) in load_missions().items():
        mission_file = km_lookup.load(mission, source=str(ROOT))
        mission_name = mission_file["mission"]["name"].lower()
        known_sources = {tutorial.get("source") for tutorial in mission_file.get("tutorials") or []}
        stubs = []
        for via, items in live.items():
            for name, description in sorted(items.items()):
                if mission in name.lower() and (via, name.lower()) not in known:
                    stubs.append(f"- {{via: {via}, name: {name}}}  # {description}")
        for bucket in sorted({path.split("/")[0] for path in s3_paths}):
            for top in s3_directories(bucket):
                for path in [top] if not is_covered(top, s3_paths) else s3_directories(top):
                    if not is_covered(path, s3_paths):
                        stubs.append(f'- {{via: s3, name: "{path}"}}  # S3 prefix not in the knowledge map')
        for notebook in notebooks:
            if notebook.get("section", "").lower() == mission_name and notebook["file"] not in known_sources:
                stubs.append(f'- {{title: "{notebook["title"]}", url: "{page_url(notebook["file"])}", '
                             f'source: {notebook["file"]}, uses: []}}  # new tutorial: fill in `uses`')
        report[mission] = stubs
    return report


def to_markdown(report):
    total = sum(len(stubs) for stubs in report.values())
    checked = f"Last checked {date.today().isoformat()}."
    if not total:
        return f"Nothing new: every live collection, table, S3 prefix and mission tutorial is in the knowledge map. {checked}\n"
    lines = [checked, (f"{total} item(s) IRSA lists that the knowledge map doesn't. In `missions/<mission>.yaml`, add "
             "`via` lines under the right dataset's `access` and tutorial lines under `tutorials`; "
             "each leaves this list on "
             "the next run.\n")]
    for mission, stubs in report.items():
        if stubs:
            lines += [f"## {mission}\n", "```yaml", *stubs, "```\n"]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-o", "--output", type=Path, help="also write the report to this file")
    args = parser.parse_args(argv)

    markdown = to_markdown(discover())
    print(markdown)
    if args.output:
        args.output.write_text(markdown)


if __name__ == "__main__":
    main()
