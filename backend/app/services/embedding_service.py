import hashlib
import logging
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from app.config import MODEL_NAME

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self, texts: list[str], cache_dir: Path):
        self.texts = texts
        self.cache_dir = cache_dir
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), norm="l2")
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        self.backend = "sentence-transformers"
        self.model = None
        self.product_embeddings = self._load_or_create_embeddings()

    def _cache_file(self) -> Path:
        fingerprint = hashlib.sha256((MODEL_NAME + "\n" + "\n".join(self.texts)).encode()).hexdigest()[:16]
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        return self.cache_dir / f"products-{fingerprint}.npy"

    def _load_or_create_embeddings(self) -> np.ndarray:
        cache_file = self._cache_file()
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer(MODEL_NAME)
            if cache_file.exists():
                return np.load(cache_file)
            embeddings = self.model.encode(self.texts, normalize_embeddings=True, show_progress_bar=False)
            np.save(cache_file, embeddings.astype("float32"))
            return embeddings
        except Exception as error:  # Model download/cache availability must not take down the API.
            self.backend = "tfidf-fallback"
            logger.warning("SentenceTransformer unavailable; using TF-IDF fallback: %s", error)
            return self.tfidf_matrix.toarray().astype("float32")

    def semantic_scores(self, query: str) -> np.ndarray:
        if self.model is not None:
            query_vector = self.model.encode([query], normalize_embeddings=True, show_progress_bar=False)[0]
            return np.clip(self.product_embeddings @ query_vector, 0, 1)
        query_vector = self.vectorizer.transform([query]).toarray()[0]
        return np.clip(self.product_embeddings @ query_vector, 0, 1)

    def lexical_scores(self, query: str) -> np.ndarray:
        query_vector = self.vectorizer.transform([query])
        return (self.tfidf_matrix @ query_vector.T).toarray().ravel().clip(0, 1)
