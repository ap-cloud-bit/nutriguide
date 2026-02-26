"""
/mealplan routes — AI-powered meal planning via Claude.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from models.schemas import MealPlanRequest, MealPlanResponse
from core.ai_client import generate_meal_plan_ai

router = APIRouter()


@router.post("/generate", response_model=MealPlanResponse)
async def generate_meal_plan(request: MealPlanRequest):
    """
    Generate a personalized AI meal plan based on user profile, budget, and pantry.
    Powered by Claude — returns a full week of meals with cost estimates and shopping list.
    """
    user_profile = {
        "age":          request.age,
        "goal":         request.goal.value,
        "budget_level": request.budget_level.value,
        "preferences":  request.preferences,
        "allergies":    request.allergies,
        "pantry_items": request.pantry_items,
    }

    try:
        plan_text = generate_meal_plan_ai(user_profile, request.duration_days)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI meal plan generation failed: {str(e)}. Check ANTHROPIC_API_KEY.",
        )

    # Extract cost estimate from AI text (Claude usually mentions it)
    estimated_cost = "See plan details below"
    for line in plan_text.split("\n"):
        if "$" in line or "cost" in line.lower() or "budget" in line.lower():
            if any(char.isdigit() for char in line):
                estimated_cost = line.strip("- •").strip()
                break

    return MealPlanResponse(
        duration_days=request.duration_days,
        plan_text=plan_text,
        estimated_cost=estimated_cost,
        generated_at=datetime.utcnow().isoformat() + "Z",
    )
