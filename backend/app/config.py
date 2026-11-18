from pathlib import Path
import os


def parse_cors_origins(value: str) -> list[str]:
    return [
        origin.strip().strip("()").rstrip("/")
        for origin in value.split(",")
        if origin.strip().strip("()").rstrip("/")
    ]


BACKEND_DIR = Path(__file__).resolve().parents[1]
PRODUCTS_PATH = Path(os.getenv("PRODUCTS_PATH", BACKEND_DIR / "products.json"))
CACHE_DIR = Path(os.getenv("CACHE_DIR", BACKEND_DIR / ".cache"))
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
MIN_RELEVANCE_SCORE = float(os.getenv("MIN_RELEVANCE_SCORE", "0.20"))
CORS_ORIGINS = parse_cors_origins(
    os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
)
