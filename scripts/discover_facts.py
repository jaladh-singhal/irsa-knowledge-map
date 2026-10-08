#!/usr/bin/env python3
"""Find IRSA collections, tables and S3 prefixes that the knowledge map doesn't list yet.

Compares what IRSA lists live (SIA/SSA collections and TAP tables via astroquery, top-level
prefixes of each mission's S3 buckets) against the `access` entries in the mission files.
A live item counts as known only if the same service lists it (e.g. `via: sia`), and a
collection or table belongs to a mission when its name contains the mission id.

Prints a Markdown report with a ready-to-paste YAML line per new item, and writes it to
--output if given. Exit code is 0 whether or not anything new is found.
"""

import argparse
from datetime import date
from pathlib import Path

import s3fs
import yaml
from astroquery.ipac.irsa import Irsa

ROOT = Path(__file__).resolve().parent.parent / "knowledge-map"


def load_missions():
    """Map mission id -> (known (via, name) pairs, known S3 top-level prefixes)."""
    missions = {}
    for path in sorted((ROOT / "missions").glob("*.yaml")):
        mission_file = yaml.safe_load(path.read_text())
        known, s3_prefixes = set(), set()
        for collection in mission_file.get("collections") or []:
            for dataset in collection.get("datasets") or []:
                for entry in dataset.get("access") or []:
                    name = str(entry.get("name") or "")
                    known.add((entry["via"], name.lower()))
                    if entry["via"] in ("s3", "hats"):
                        bucket, _, prefix = name.removeprefix("s3://").partition("/")
                        s3_prefixes.add((bucket, prefix.split("/")[0] + "/"))
        missions[mission_file["mission"]["id"]] = (known, s3_prefixes)
    return missions


def s3_top_level(bucket):
    """Top-level directory prefixes of a bucket, e.g. ["qr2/", "qr3/"] (files like index.html excluded)."""
    entries = s3fs.S3FileSystem(anon=True).ls(bucket, detail=True, refresh=True)
    return [entry["name"].removeprefix(f"{bucket}/") + "/" for entry in entries if entry["type"] == "directory"]


def discover():
    """Return {mission id: [YAML stub lines for items not in the knowledge map]}."""
    live = {
        "sia": {name: "SIA collection" for name in Irsa.list_collections(servicetype="SIA")["collection"]},
        "ssa": {name: "SSA collection" for name in Irsa.list_collections(servicetype="SSA")["collection"]},
        "tap": Irsa.list_catalogs(include_metadata_tables=True),  # table name -> description
    }
    report = {}
    for mission, (known, s3_prefixes) in load_missions().items():
        stubs = []
        for via, items in live.items():
            for name, description in sorted(items.items()):
                if mission in name.lower() and (via, name.lower()) not in known:
                    stubs.append(f"- {{via: {via}, name: {name}}}  # {description}")
        for bucket in sorted({bucket for bucket, _ in s3_prefixes}):
            for prefix in s3_top_level(bucket):
                if (bucket, prefix) not in s3_prefixes:
                    stubs.append(f'- {{via: s3, name: "{bucket}/{prefix}"}}  # new top-level S3 prefix')
        report[mission] = stubs
    return report


def to_markdown(report):
    total = sum(len(stubs) for stubs in report.values())
    checked = f"Last checked {date.today().isoformat()}."
    if not total:
        return f"Nothing new: every live collection, table and S3 prefix is in the knowledge map. {checked}\n"
    lines = [checked, (f"{total} item(s) IRSA lists that the knowledge map doesn't. Add each under the right "
             "dataset's `access` in `knowledge-map/missions/<mission>.yaml`; it leaves this list on "
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
