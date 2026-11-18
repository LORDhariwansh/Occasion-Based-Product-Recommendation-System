from pydantic import BaseModel, Field, field_validator


class RecommendationRequest(BaseModel):
    occasion: str = Field(min_length=2, max_length=300, description="Natural-language gifting occasion")
    top_k: int = Field(default=5, ge=1, le=10)

    @field_validator("occasion")
    @classmethod
    def occasion_must_contain_words(cls, value: str) -> str:
        cleaned = " ".join(value.split())
        if not cleaned:
            raise ValueError("occasion cannot be blank")
        return cleaned


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    short_description: str
    brand: str
    category_id: str
    price: float | None
    image: str | None
    stock: int


class Recommendation(ProductResponse):
    similarity_score: float
    reason: str


class RecommendationResponse(BaseModel):
    occasion: str
    total_results: int
    recommendations: list[Recommendation]
    message: str | None = None


class HealthResponse(BaseModel):
    status: str
    eligible_products: int
    embedding_backend: str
