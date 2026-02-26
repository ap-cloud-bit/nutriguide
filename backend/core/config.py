"""
Configuration — reads from .env file.

Setup:
    cp .env.example .env
    # Edit .env and add your ANTHROPIC_API_KEY
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Required ────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

# ── Optional ─────────────────────────────────────────────────────────────────
DATABASE_URL: str = os.getenv("DATABASE_URL", "")
SECRET_KEY:   str = os.getenv("SECRET_KEY", "change-me-in-production")

# ── External APIs (no key required) ──────────────────────────────────────────
OFF_BASE_URL: str = "https://world.openfoodfacts.org/api/v2"

# ── Rate limits (requests per minute) ────────────────────────────────────────
RATE_FOOD:     int = 20
RATE_MEALPLAN: int = 5
RATE_AI_CHAT:  int = 60
RATE_SHOPPING: int = 10
