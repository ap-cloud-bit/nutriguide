"""
NutriGuide — AI Food Intelligence Agent
Backend API v1.0.0

Run locally:
    uvicorn main:app --reload

Production:
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os

from routes import food, mealplan, ai_chat, user, shopping


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup checks
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key or api_key == "your_anthropic_api_key_here":
        print("⚠️  WARNING: ANTHROPIC_API_KEY not set — AI features will fail.")
        print("   Add it to your .env file. Get one at: https://console.anthropic.com")
    else:
        print("✅ Anthropic API key detected.")
    print("🥦 NutriGuide API is ready at http://localhost:8000")
    print("📖 Interactive docs at  http://localhost:8000/docs")
    yield
    print("NutriGuide API shutting down...")


app = FastAPI(
    title="NutriGuide API",
    description=(
        "AI Food Intelligence Agent — eat healthier, safer, cheaper.\n\n"
        "**Try these barcodes in /food/scan:**\n"
        "- `3017620422003` (Nutella)\n"
        "- `5000159484763` (Kit Kat)\n"
        "- `0038000138690` (Kellogg's Corn Flakes)\n"
        "- `8710398525406` (Quaker Oats)"
    ),
    version="1.0.0",
    contact={
        "name": "Awais Shakeel Pasha",
        "url": "https://github.com/ap-cloud-bit/nutriguide",
    },
    license_info={"name": "MIT"},
    lifespan=lifespan,
)

# CORS — allow frontend (Vercel) to call backend (Railway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # In production: ["https://yourapp.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ─────────────────────────────────────────────────────────────────
app.include_router(user.router,     prefix="/user",     tags=["👤 User"])
app.include_router(food.router,     prefix="/food",     tags=["📷 Food Scanner"])
app.include_router(mealplan.router, prefix="/mealplan", tags=["📋 Meal Planner"])
app.include_router(shopping.router, prefix="/shopping", tags=["🛒 Shopping"])
app.include_router(ai_chat.router,  prefix="/ai",       tags=["💬 AI Chat"])


@app.get("/", tags=["🏥 Health"], summary="API Info")
async def root():
    """Returns API status and available endpoints."""
    return {
        "service":     "NutriGuide API",
        "version":     "1.0.0",
        "status":      "healthy",
        "docs":        "/docs",
        "endpoints": {
            "scan_food":       "POST /food/scan",
            "generate_plan":   "POST /mealplan/generate",
            "chat":            "POST /ai/chat",
            "optimize_cart":   "POST /shopping/optimize-cart",
            "create_user":     "POST /user/create",
        },
    }


@app.get("/health", tags=["🏥 Health"], summary="Health Check")
async def health_check():
    """Simple liveness probe for Railway/Render health checks."""
    return {"status": "ok"}


@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "docs": "/docs"},
    )


@app.exception_handler(500)
async def server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "hint": "Check that ANTHROPIC_API_KEY is set in your .env file",
        },
    )
