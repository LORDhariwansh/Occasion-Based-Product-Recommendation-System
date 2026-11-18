from fastapi import APIRouter, HTTPException, Request

from app.schemas.recommendation import ProductResponse, RecommendationRequest, RecommendationResponse

router = APIRouter(tags=["recommendations"])


@router.get("/products", response_model=list[ProductResponse])
def products(request: Request) -> list[dict]:
    return [{
        "id": p.id, "name": p.name, "description": p.description, "short_description": p.short_description,
        "brand": p.brand, "category_id": p.category_id, "price": p.price, "image": p.image, "stock": p.stock,
    } for p in request.app.state.recommender.products]


@router.post("/recommend", response_model=RecommendationResponse)
def recommend(payload: RecommendationRequest, request: Request) -> RecommendationResponse:
    recommender = request.app.state.recommender
    results = recommender.recommend(payload.occasion, payload.top_k)
    message = None if results else "No suitably relevant eligible products were found for this occasion."
    return RecommendationResponse(occasion=payload.occasion, total_results=len(results), recommendations=results, message=message)
