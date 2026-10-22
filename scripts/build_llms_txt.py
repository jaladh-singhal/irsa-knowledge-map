#!/usr/bin/env python3
"""Write a mission's llms.txt (https://llmstxt.org) from the knowledge map, to stdout.

It lists the mission's releases and, for each dataset, the names, paths and links to query it
with, plus IRSA's services, tutorials, tools, identifiers and docs: the facts an assistant needs
to point someone at the right data. Reads the map like km_lookup.py (GitHub main, or KM_SOURCE).

    python scripts/build_llms_txt.py euclid > llms.txt
"""

import argparse
import sys
from datetime import date
from pathlib import Path

# km_lookup.py sits at the repo root, or next to this script when the two are fetched on their own
sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parent.parent)]
import km_lookup  # noqa: E402


REPO_URL = "https://github.com/jaladh-singhal/irsa-knowledge-map"


def value(via, name):
    """An access entry's name as Markdown: links for URLs, s3:// for S3 paths, code otherwise."""
    if name.startswith("http"):
        return f"<{name}>"
    if via in ("s3", "hats"):
        return f"`s3://{name.removeprefix('s3://')}`"
    return f"`{name}`"


def access_line(entries):
    """Access entries as `<service key> <name>`, the keys listed under IRSA services."""
    parts = []
    for entry in entries:
        text = entry["via"]
        if entry.get("name"):
            text += f" {value(entry['via'], entry['name'])}"
        if entry.get("status") == "planned":
            text += " (planned)"
        parts.append(text)
    return "; ".join(parts)


def dataset_line(dataset):
    line = f"- **{dataset['name']}** (`{dataset['id']}`, {dataset.get('type', 'data')})"
    if dataset.get("access"):
        line += ": " + access_line(dataset["access"])
    if dataset.get("doi"):
        line += f"; DOI [{dataset['doi']}](https://doi.org/{dataset['doi']})"
    if (dataset.get("files") or {}).get("pattern"):
        line += f"; files `{dataset['files']['pattern']}`"
    return line


def build(mission_name, source=None):
    mission_data = km_lookup.load(mission_name, source)
    services = km_lookup.services(source)
    mission = mission_data["mission"]
    lines = [
        f"# {mission['name']} at IRSA",
        "",
        f"> Where {mission['name']} data lives at the NASA/IPAC Infrared Science Archive (IRSA) and how to "
        "query it: release status, and each dataset's query names, paths, DOIs and tutorials. Generated "
        f"from the [IRSA knowledge map]({REPO_URL}) "
        f"on {date.today().isoformat()}; its names and links are checked against IRSA's live services weekly. "
        "A name missing here is not confirmed, not proof it doesn't exist: check `Irsa.list_collections()` "
        "and `Irsa.list_catalogs()` in astroquery before concluding.",
        "",
        f"{mission['name']}: {mission.get('agency', '')}, launched {mission.get('launch', 'n/a')}. "
        f"IRSA's mission page: <{mission.get('archive_page', '')}>.",
        "",
        "## IRSA services",
        "",
        "Datasets below list how to reach them as `<service key> <name>`, e.g. `sia euclid_DpdMerBksMosaic`.",
        "",
    ]
    for via, service in services.items():
        details = [f"`{service['endpoint']}`" if service.get("endpoint") else "",
                   service.get("usage", ""), f"Python: {service['python']}" if service.get("python") else "",
                   f"docs <{service['docs']}>" if service.get("docs") else ""]
        details = "; ".join(part for part in details if part)
        lines.append(f"- `{via}`: {service['name']}" + (f" ({details})" if details else ""))

    lines += ["", "## Releases", "", "| Release | Id | Kind | Status | Released | Overview |", "| --- | --- | --- | --- | --- | --- |"]
    for collection in mission_data["collections"]:
        overview = f"<{collection['overview']}>" if collection.get("overview") else ""
        released = str(collection.get("released") or "")
        if released and collection.get("status") == "planned":
            released += " (expected)"
        lines.append(f"| {collection['name']} | `{collection['id']}` | {collection.get('kind', '')} | "
                     f"{collection.get('status', '')} | {released} | {overview} |")

    for collection in mission_data["collections"]:
        if not (collection.get("datasets") or collection.get("access") or collection.get("notes")):
            continue
        lines += ["", f"## {collection['name']} (`{collection['id']}`, {collection.get('status', '')})", ""]
        lines += [f"- {note}" for note in collection.get("notes") or []]
        if collection.get("access"):
            lines.append("- Release roots: " + access_line(collection["access"]))
        lines += [dataset_line(dataset) for dataset in collection.get("datasets") or []]

    sections = [
        ("Tutorials", "tutorials", lambda entry: f"- [{entry['title']}]({entry['url']}): uses "
         + (", ".join(f"`{used}`" for used in entry.get("uses") or []) or "no listed dataset")),
        ("Tools", "tools", lambda entry: f"- [{entry['name']}]({entry['url']}): {entry.get('use_for', '')}"),
        ("Identifiers", "identifiers", lambda entry: f"- **{entry['name']}**: {entry.get('description', '')}"
         + (f" (e.g. `{entry['example']}`)" if entry.get("example") else "")),
        ("Docs", "docs", lambda entry: f"- [{entry['title']}]({entry['url']})"),
        ("Known issues", "known_issues", lambda entry: f"- {entry.get('title', '')}: {entry.get('summary', '')}"),
    ]
    for heading, key, format_entry in sections:
        entries = mission_data.get(key) or []
        if entries:
            lines += ["", f"## {heading}", ""] + [format_entry(entry) for entry in entries]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("mission", help="mission file name, e.g. euclid")
    parser.add_argument("--source", help="base URL or local checkout of the map (default: KM_SOURCE or GitHub main)")
    args = parser.parse_args(argv)
    sys.stdout.write(build(args.mission, args.source))


if __name__ == "__main__":
    main()
