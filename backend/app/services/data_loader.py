import json
from pathlib import Path
from typing import Any


def load_catalog(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as source:
        payload = json.load(source)
    if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
        raise ValueError("products.json must contain a JSON array of product objects")
    return payload
