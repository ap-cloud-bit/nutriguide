"""
/user routes — user creation and profile management.
Note: In production, connect to PostgreSQL via SQLAlchemy.
For this demo, we use in-memory storage so you can run without a database.
"""

import uuid
import hashlib
from fastapi import APIRouter, HTTPException
from models.schemas import UserCreate, UserResponse

router = APIRouter()

# In-memory store (replace with PostgreSQL in production)
_users_db: dict = {}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@router.post("/create", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    """
    Create a new NutriGuide user profile.
    """
    # Check duplicate email
    for u in _users_db.values():
        if u["email"] == user.email:
            raise HTTPException(status_code=409, detail="Email already registered.")

    user_id = str(uuid.uuid4())
    _users_db[user_id] = {
        "user_id":      user_id,
        "email":        user.email,
        "password_hash": hash_password(user.password),
        "age":          user.age,
        "gender":       user.gender,
        "height_cm":    user.height_cm,
        "weight_kg":    user.weight_kg,
        "budget_level": user.budget_level.value,
        "goal":         user.goal.value,
        "preferences":  user.preferences,
        "allergies":    user.allergies,
    }

    return UserResponse(
        user_id=user_id,
        email=user.email,
        age=user.age,
        budget_level=user.budget_level.value,
        goal=user.goal.value,
        preferences=user.preferences,
        allergies=user.allergies,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get a user profile by ID."""
    user = _users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return UserResponse(**{k: v for k, v in user.items() if k != "password_hash"})
