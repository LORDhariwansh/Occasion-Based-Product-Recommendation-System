import re
from typing import Iterable

import numpy as np

from app.config import MIN_RELEVANCE_SCORE
from app.services.embedding_service import EmbeddingService
from app.services.preprocessing import Product

OCCASION_TERMS = {
    "birthday": "birthday gift celebration present",
    "wedding": "wedding present celebration gift",
    "diwali": "diwali festive celebration gift",
    "valentine": "valentine romantic love gift",
    "anniversary": "anniversary romantic celebration gift",
    "corporate": "corporate employee colleague professional gift",
    "colleague": "colleague professional office gift",
}
STOP_WORDS = {"a", "an", "for", "the", "my", "to", "with", "gift", "gifts", "present", "something", "under"}


def _budget_from_query(query: str) -> float | None:
    match = re.search(r"(?:under|below|less than|within)\s*(?:₹|rs\.?|inr)?\s*([\d,]+)", query, re.I)
    return float(match.group(1).replace(",", "")) if match else None


def _expanded_query(query: str) -> str:
    lowered = query.lower()
    extras = [terms for token, terms in OCCASION_TERMS.items() if token in lowered]
    return f"{query} {' '.join(extras)}".strip()


def _tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-zA-Z]{3,}", text.lower()) if token not in STOP_WORDS}


class Recommender:
    def __init__(self, products: list[Product], embedding_service: EmbeddingService):
        self.products = products
        self.embeddings = embedding_service

    @property
    def embedding_backend(self) -> str:
        return self.embeddings.backend

    def recommend(self, occasion: str, top_k: int) -> list[dict]:
        query = _expanded_query(occasion)
        semantic = self.embeddings.semantic_scores(query)
        lexical = self.embeddings.lexical_scores(query)
        query_terms = _tokens(occasion)
        title_scores = np.array([len(query_terms & _tokens(product.name)) / max(1, len(query_terms)) for product in self.products])
        scores = 0.65 * semantic + 0.22 * lexical + 0.13 * title_scores
        budget = _budget_from_query(occasion)
        indices: Iterable[int] = np.argsort(scores)[::-1]
        price_only = budget is not None and not query_terms
        if price_only:
            indices = sorted(range(len(self.products)), key=lambda index: self.products[index].price if self.products[index].price is not None else float("inf"))
        recommendations: list[dict] = []
        for index in indices:
            product = self.products[int(index)]
            if budget is not None and (product.price is None or product.price > budget):
                continue
            score = float(scores[index])
            if not price_only and score < MIN_RELEVANCE_SCORE:
                break
            recommendations.append({
                "id": product.id, "name": product.name, "description": product.description,
                "short_description": product.short_description, "brand": product.brand,
                "category_id": product.category_id, "price": product.price, "image": product.image,
                "stock": product.stock, "similarity_score": round(score if not price_only else 0.0, 3),
                "reason": self._reason(product, query_terms, budget, price_only),
            })
            if len(recommendations) == top_k:
                break
        return recommendations

    @staticmethod
    def _reason(product: Product, query_terms: set[str], budget: float | None, price_only: bool) -> str:
        if price_only:
            return f"Fits the ₹{budget:,.0f} price ceiling; no occasion-specific ranking was provided."
        product_terms = _tokens(f"{product.name} {product.brand} {product.short_description} {product.description}")
        matches = sorted(query_terms & product_terms)
        if matches:
            reason = f"Matches '{', '.join(matches[:3])}' in the catalog details."
        else:
            reason = "Semantically related to the occasion based on its catalog title and description."
        if budget is not None:
            reason += f" Priced within the ₹{budget:,.0f} budget."
        return reason
