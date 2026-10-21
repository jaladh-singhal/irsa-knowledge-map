"""Example helper for walking the IRSA knowledge map.

The YAML nests collection -> dataset -> access entries, and each access entry's `via`
names a service in irsa.yaml. A collection is a release (Euclid Q1, SPHEREx QR3) or
another group of datasets (kind: ancillary, target_view, contributed). Dataset ids are
<mission>.<collection>.<product>, and a product keeps its key in every collection that
has it, so `names(euclid, "q1", "mer-catalog", "tap")` and
`names(euclid, "dr1", "mer-catalog", "tap")` ask for the same product in two releases.

Needs only pyyaml. Reads the raw files from GitHub by default, or from `source` (a base URL or
a local checkout), or from the KM_SOURCE environment variable if `source` isn't given.
"""

import os
from pathlib import Path
from urllib.request import urlopen

import yaml

RAW_MAIN = "https://raw.githubusercontent.com/jaladh-singhal/irsa-knowledge-map/main/"


def _source(source):
    """`source` if given, else KM_SOURCE from the environment, else GitHub main."""
    return source or os.environ.get("KM_SOURCE") or RAW_MAIN


def _read(relative_path, source):
    source = _source(source)
    if source.startswith(("http://", "https://")):
        with urlopen(source.rstrip("/") + "/" + relative_path) as response:
            return yaml.safe_load(response.read())
    return yaml.safe_load((Path(source) / relative_path).read_text())


def load(mission, source=None):
    """One mission file as a dict, e.g. load("euclid"). `source` is a base URL or a local folder."""
    mission_data = _read(f"missions/{mission}.yaml", source)
    mission_data["_source"] = _source(source)   # so tutorials() reads irsa.yaml from the same place
    return mission_data


def services(source=None):
    """The shared services from irsa.yaml, keyed by `via` (e.g. "sia", "tap", "s3")."""
    return _read("irsa.yaml", source)["services"]


def collections(mission_data, kind=None):
    """(id, kind, status) of each collection, optionally only one kind, e.g. kind="release"."""
    return [(collection["id"], collection.get("kind"), collection.get("status"))
            for collection in mission_data["collections"] if kind in (None, collection.get("kind"))]


def products(mission_data):
    """The mission's declared product keys, e.g. {"mer-catalog": {...}, ...}."""
    return {product["key"]: product for product in mission_data.get("products") or []}


def iter_access(mission_data):
    """Every (collection, dataset, access entry) in the mission, in file order."""
    for collection in mission_data["collections"]:
        for dataset in collection.get("datasets") or []:
            for entry in dataset.get("access") or []:
                yield collection, dataset, entry


def dataset(mission_data, collection, product):
    """The dataset `<mission>.<collection>.<product>`, or None if the knowledge map doesn't list it."""
    dataset_id = f"{mission_data['mission']['id']}.{collection}.{product}"
    for group in mission_data["collections"]:
        for candidate in group.get("datasets") or []:
            if candidate["id"] == dataset_id:
                return candidate
    return None


def tutorials(mission_data, collection=None, product=None):
    """Tutorials that use a dataset (or all of the mission's), with `source_url` added.

    `url` is the published page; `source_url` is the raw notebook (MyST Markdown), built from
    irsa.yaml's tutorials.source_prefix + the tutorial's `source` path.
    """
    prefix = _read("irsa.yaml", mission_data.get("_source"))["tutorials"]["source_prefix"]
    wanted = None if product is None else f"{mission_data['mission']['id']}.{collection}.{product}"
    return [dict(tutorial, source_url=prefix + tutorial["source"])
            for tutorial in mission_data.get("tutorials") or []
            if wanted is None or wanted in tutorial.get("uses", [])]


def names(mission_data, collection, product, via):
    """Names a product is served under for one service, e.g. its TAP table or S3 prefix.

    Returns [] if the product or service isn't listed. That means "not confirmed", not
    "doesn't exist": check IRSA live before concluding, and never guess a name.
    """
    found = dataset(mission_data, collection, product)
    if found is None:
        return []
    return [entry["name"] for entry in found.get("access") or [] if entry["via"] == via and entry.get("name")]
