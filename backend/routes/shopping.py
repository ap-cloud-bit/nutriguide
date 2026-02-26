"""
POST /shopping/optimize-cart — AI-powered cart optimization.
"""

from fastapi import APIRouter, HTTPException
from models.schemas import ShoppingOptimizeRequest, ShoppingOptimizeResponse
from core.ai_client import optimize_shopping_ai

router = APIRouter()


@router.post(
    "/optimize-cart",
    response_model=ShoppingOptimizeResponse,
    summary="Optimize a shopping cart",
    description="Submit a shopping list and get healthier, cheaper alternatives powered by Claude AI.",
)
async def optimize_cart(request: ShoppingOptimizeRequest):
    if not request.items:
        raise HTTPException(status_code=400, detail="items list cannot be empty.")

    items_text = "\n".join(
        f"- {item.name} ({item.quantity})" for item in request.items
    )

    try:
        tips = optimize_shopping_ai(items_text, request.budget_level.value)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

    optimized = [
        {
            "name":     item.name,
            "quantity": item.quantity,
            "note":     "See AI tips above",
        }
        for item in request.items
    ]

    return ShoppingOptimizeResponse(
        optimized_list=optimized,
        tips=tips,
        estimated_savings="See AI analysis above",
    )
