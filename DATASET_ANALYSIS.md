# Dataset analysis

Analysis source: the supplied `products.json` file. The original source file was not modified; the application uses the copied runtime catalog at `backend/products.json`.

## Shape and quality

| Check | Result |
| --- | ---: |
| Root structure | JSON array |
| Total records | 110 |
| Unique IDs | 110 |
| Unique SKUs | 110 |
| Repeated product names | 2 duplicate-name rows, retained because their record IDs differ |
| Category IDs | 20 |
| Brands | 16 |
| Missing description, short description, brand, price, image | 0 each |
| Malformed prices | 0 |
| Zero or negative stock | 0 |
| Soft-deleted records | 0 |
| `mainImage` values | 110 HTTPS URLs |
| `files` arrays | Not present in this catalog |

The actual schema is a flat object with `id`, `shopId`, `categoryId`, `name`, `slug`, `description`, `shortDescription`, `mainImage`, `brand`, `sku`, `price`, `stock`, `isApproved`, `status`, `deletedAt`, and operational fields. It has no `files` field and no embedded image payload. `categoryId` is an opaque identifier, so the application deliberately does not invent category names.

## Recommendation eligibility

The preprocessing rule is:

```text
isApproved == true AND status == "ACTIVE" AND stock > 0 AND deletedAt is null
```

This keeps 104 products. Six records are excluded: four are `REVIEW_REQUIRED` and two are `DRAFT`; all six are also unapproved. Prices are numeric strings in the source and are normalized to numbers without changing the original ID or source catalog.
