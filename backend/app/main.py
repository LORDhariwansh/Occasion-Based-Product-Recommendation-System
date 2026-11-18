import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CACHE_DIR, CORS_ORIGINS, PRODUCTS_PATH
from app.routes.recommendations import router
from app.schemas.recommendation import HealthResponse
from app.services.data_loader import load_catalog
from app.services.embedding_service import EmbeddingService
from app.services.preprocessing import preprocess_products
from app.services.recommender import Recommender

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    products = preprocess_products(load_catalog(PRODUCTS_PATH))
    if not products:
        raise RuntimeError("No eligible products found after preprocessing")
    embeddings = EmbeddingService([product.searchable_text for product in products], CACHE_DIR)
    app.state.recommender = Recommender(products, embeddings)
    logger.info("Loaded %d eligible products using %s", len(products), embeddings.backend)
    yield


app = FastAPI(title="Occasion Product Recommender", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)


@app.get("/", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    recommender = app.state.recommender
    return HealthResponse(status="ok", eligible_products=len(recommender.products), embedding_backend=recommender.embedding_backend)
