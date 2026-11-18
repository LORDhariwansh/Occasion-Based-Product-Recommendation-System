import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any


def normalize_text(value: Any) -> str:
    return " ".join(str(value or "").replace("\r", " ").replace("\n", " ").split())


def parse_price(value: Any) -> float | None:
    cleaned = re.sub(r"[^0-9.\-]", "", str(value or ""))
    try:
        result = Decimal(cleaned)
        return float(result) if result >= 0 else None
    except (InvalidOperation, ValueError):
        return None


def parse_stock(value: Any) -> int:
    try:
        return max(0, int(float(value)))
    except (TypeError, ValueError):
        return 0


def normalize_image(value: Any) -> str | None:
    if isinstance(value, str):
        return normalize_text(value) or None
    if isinstance(value, dict):
        for key in ("url", "fileUrl", "path", "location", "src"):
            image = normalize_text(value.get(key))
            if image:
                return image
    return None


def extract_image(record: dict[str, Any]) -> str | None:
    main_image = normalize_image(record.get("mainImage"))
    if main_image:
        return main_image
    files = record.get("files")
    if not isinstance(files, list):
        return None
    primary_files = [
        item
        for item in files
        if isinstance(item, dict) and (item.get("isPrimary") or item.get("primary") or item.get("is_primary"))
    ]
    for item in [*primary_files, *files]:
        image = normalize_image(item)
        if image:
            return image
    return None


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    description: str
    short_description: str
    brand: str
    category_id: str
    price: float | None
    image: str | None
    stock: int
    searchable_text: str


def preprocess_products(records: list[dict[str, Any]]) -> list[Product]:
    products: list[Product] = []
    seen_ids: set[str] = set()
    for record in records:
        product_id = normalize_text(record.get("id") or record.get("productId"))
        if not product_id or product_id in seen_ids:
            continue
        seen_ids.add(product_id)
        is_active = normalize_text(record.get("status")).upper() == "ACTIVE"
        if not (record.get("isApproved") is True and is_active and record.get("deletedAt") is None):
            continue
        stock = parse_stock(record.get("stock"))
        if stock <= 0:
            continue
        name = normalize_text(record.get("name") or record.get("title"))
        description = normalize_text(record.get("description"))
        short_description = normalize_text(record.get("shortDescription"))
        brand = normalize_text(record.get("brand"))
        category_id = normalize_text(record.get("categoryId") or record.get("vendor_category"))
        image = extract_image(record)
        searchable_text = " ".join(part for part in (name, name, brand, short_description, description, category_id) if part)
        if not name or not searchable_text:
            continue
        products.append(Product(product_id, name, description, short_description, brand, category_id, parse_price(record.get("price")), image, stock, searchable_text))
    return products
