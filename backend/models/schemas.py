"""
Pydantic schemas — request and response models for NutriGuide API.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum


class BudgetLevel(str, Enum):
    low    = "low"
    medium = "medium"
    high   = "high"


class DietGoal(str, Enum):
    fat_loss    = "fat-loss"
    muscle_gain = "muscle-gain"
    balanced    = "balanced"
    glp1        = "glp1"


# ── User ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email:        EmailStr
    password:     str = Field(min_length=8)
    age:          Optional[int] = None
    gender:       Optional[str] = None
    height_cm:    Optional[int] = None
    weight_kg:    Optional[float] = None
    budget_level: BudgetLevel = BudgetLevel.medium
    goal:         DietGoal    = DietGoal.balanced
    preferences:  List[str]   = []
    allergies:    List[str]   = []


class UserResponse(BaseModel):
    user_id:      str
    email:        str
    age:          Optional[int]
    budget_level: str
    goal:         str
    preferences:  List[str]
    allergies:    List[str]


# ── Food Scan ─────────────────────────────────────────────────────────────────

class FoodScanRequest(BaseModel):
    barcode: str = Field(..., description="EAN/UPC barcode number")


class FoodScanResponse(BaseModel):
    barcode:          str
    product_name:     str
    brand:            str
    health_score:     float          # 0–10
    upf_level:        int            # NOVA group 1–4
    nutriscore:       str            # A–E
    calories_100g:    Optional[float]
    protein_100g:     Optional[float]
    sugar_100g:       Optional[float]
    fat_100g:         Optional[float]
    ai_analysis:      str            # Claude's text analysis
    alternatives:     List[str]
    image_url:        Optional[str]


# ── Meal Plan ─────────────────────────────────────────────────────────────────

class MealPlanRequest(BaseModel):
    age:          Optional[int]   = 30
    goal:         DietGoal        = DietGoal.balanced
    budget_level: BudgetLevel     = BudgetLevel.medium
    duration_days: int            = Field(default=7, ge=1, le=14)
    preferences:  List[str]       = []
    allergies:    List[str]       = []
    pantry_items: List[str]       = []


class MealPlanResponse(BaseModel):
    duration_days: int
    plan_text:     str    # Claude's full meal plan
    estimated_cost: str
    generated_at:  str


# ── Shopping ──────────────────────────────────────────────────────────────────

class ShoppingItem(BaseModel):
    name:     str
    quantity: str


class ShoppingOptimizeRequest(BaseModel):
    items:        List[ShoppingItem]
    budget_level: BudgetLevel = BudgetLevel.medium


class ShoppingOptimizeResponse(BaseModel):
    optimized_list: List[dict]
    tips:           str
    estimated_savings: str


# ── AI Chat ───────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role:    str   # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    user_context: Optional[dict] = None


class ChatResponse(BaseModel):
    reply:      str
    model_used: str = "claude-haiku-4-5"
