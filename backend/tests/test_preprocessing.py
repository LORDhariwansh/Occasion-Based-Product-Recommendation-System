from app.services.preprocessing import preprocess_products


def test_preprocessing_filters_unavailable_and_duplicate_ids():
    records = [
        {"id": "one", "name": "Approved", "description": "Great gift", "isApproved": True, "status": "ACTIVE", "stock": "2", "deletedAt": None, "price": "₹499"},
        {"id": "one", "name": "Duplicate", "description": "ignored", "isApproved": True, "status": "ACTIVE", "stock": 2, "deletedAt": None},
        {"id": "two", "name": "Draft", "description": "ignored", "isApproved": True, "status": "DRAFT", "stock": 2, "deletedAt": None},
        {"id": "three", "name": "Out", "description": "ignored", "isApproved": True, "status": "ACTIVE", "stock": "bad", "deletedAt": None},
    ]
    products = preprocess_products(records)
    assert len(products) == 1
    assert products[0].price == 499.0


def test_preprocessing_uses_primary_file_when_main_image_is_missing():
    records = [{
        "id": "one",
        "name": "Approved",
        "description": "Great gift",
        "isApproved": True,
        "status": "ACTIVE",
        "stock": 2,
        "deletedAt": None,
        "files": [{"url": "https://example.test/secondary.png"}, {"url": "https://example.test/primary.png", "isPrimary": True}],
    }]
    products = preprocess_products(records)
    assert products[0].image == "https://example.test/primary.png"


def test_preprocessing_keeps_products_without_an_image():
    records = [{
        "id": "one",
        "name": "Approved",
        "description": "Great gift",
        "isApproved": True,
        "status": "ACTIVE",
        "stock": 2,
        "deletedAt": None,
    }]
    products = preprocess_products(records)
    assert products[0].image is None
