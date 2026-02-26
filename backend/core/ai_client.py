"""
Claude AI client — all AI prompts and interactions for NutriGuide.

This is the brain of the app. Every AI feature calls functions from this file.
"""

import anthropic
from core.config import ANTHROPIC_API_KEY

# Lazy-init client so import doesn't fail if key is missing at startup
_client = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your_anthropic_api_key_here":
            raise ValueError(
                "ANTHROPIC_API_KEY is not set. "
                "Add it to your .env file. Get one at: https://console.anthropic.com"
            )
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


# ── System Prompt ─────────────────────────────────────────────────────────────
NUTRIGUIDE_SYSTEM_PROMPT = """You are NutriGuide — a friendly, expert AI food intelligence agent.

Your mission: help users eat healthier, safer, and cheaper by:
1. Scoring foods for health, UPF level, and safety
2. Building personalized meal plans within budget
3. Finding cheaper, healthier food alternatives
4. Answering nutrition and food safety questions clearly

Personality: warm, encouraging, science-backed — like a knowledgeable friend, not a lecture.

Rules:
- Always provide practical, actionable advice
- Back claims with real nutritional science
- Consider the user's budget, preferences, and goals
- Flag ultra-processed foods (UPF) and suggest real-food alternatives
- Never be preachy — make healthy eating feel achievable and exciting
- Do NOT reveal your internal chain-of-thought or reasoning
- Format responses with emojis where helpful to improve readability
- Keep answers concise unless the user explicitly asks for detail

Health score scale (0–10):
- 8–10: Excellent — whole, minimally processed food
- 6–7:  Good — decent choice with minor concerns
- 4–5:  Moderate — okay occasionally, has drawbacks
- 2–3:  Poor — ultra-processed, nutritionally weak
- 0–1:  Avoid — harmful additives, very high UPF score"""


# ── Core AI Function ──────────────────────────────────────────────────────────
def chat_with_nutriguide(messages: list, max_tokens: int = 1024) -> str:
    """
    Send a message list to Claude and return the text response.
    
    Args:
        messages: List of {"role": "user"|"assistant", "content": str}
        max_tokens: Maximum response length
    
    Returns:
        str: Claude's response text
    
    Raises:
        ValueError: If API key is not configured
        anthropic.APIError: If the API call fails
    """
    response = get_client().messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=max_tokens,
        system=NUTRIGUIDE_SYSTEM_PROMPT,
        messages=messages,
    )
    return response.content[0].text


# ── Specialized AI Functions ──────────────────────────────────────────────────
def generate_meal_plan_ai(user_profile: dict, duration_days: int = 7) -> str:
    """
    Generate a complete meal plan using Claude.
    
    Args:
        user_profile: Dict with age, goal, budget_level, preferences, allergies, pantry_items
        duration_days: Number of days to plan for (1–14)
    """
    pantry = ", ".join(user_profile.get("pantry_items", [])) or "none specified"
    prefs  = ", ".join(user_profile.get("preferences", [])) or "none"
    allerg = ", ".join(user_profile.get("allergies", [])) or "none"

    prompt = f"""Generate a {duration_days}-day meal plan for this user:

Profile:
- Age: {user_profile.get("age", "not specified")}
- Goal: {user_profile.get("goal", "balanced eating")}
- Budget: {user_profile.get("budget_level", "medium")} (low = <$50/wk, medium = $50–100/wk, high = $100+/wk)
- Dietary preferences: {prefs}
- Allergies / avoid: {allerg}
- Pantry items available: {pantry}

Please provide:
1. 📅 Day-by-day plan (Breakfast, Lunch, Dinner, Snack)
2. 💰 Estimated cost per day + total weekly cost
3. 💪 Daily macro summary (protein / carbs / fat targets)
4. 🛒 Shopping list for items NOT already in pantry
5. 💡 2–3 money-saving swap suggestions

Keep it practical and encouraging. Use pantry items to reduce cost."""

    return chat_with_nutriguide([{"role": "user", "content": prompt}], max_tokens=2048)


def analyze_food_ai(food_data: dict) -> str:
    """
    Get Claude's health analysis for a scanned food product.
    
    Args:
        food_data: Dict with product_name, brands, ingredients_text,
                   nutriscore_grade, nova_group, and nutriment values
    """
    prompt = f"""Analyze this food product and give a NutriGuide health assessment:

Product: {food_data.get("product_name", "Unknown")}
Brand: {food_data.get("brands", "Unknown")}
Ingredients: {str(food_data.get("ingredients_text", "Not available"))[:400]}
Nutri-Score: {str(food_data.get("nutriscore_grade", "unknown")).upper()}
NOVA Group (UPF level 1–4): {food_data.get("nova_group", "unknown")}
Per 100g:
  Calories: {food_data.get("energy_kcal_100g", "?")} kcal
  Protein:  {food_data.get("proteins_100g", "?")}g
  Sugar:    {food_data.get("sugars_100g", "?")}g
  Salt:     {food_data.get("salt_100g", "?")}g
  Fat:      {food_data.get("fat_100g", "?")}g

Please provide:
1. 🔢 Health Score (0–10) with a one-line reason
2. 🏭 UPF assessment — is it ultra-processed? Why?
3. ⚠️ Top 2 concerns (if any)
4. ✅ Top 2 positives (if any)
5. 🔄 Two healthier alternatives to consider

Be honest, brief, and helpful. No lectures."""

    return chat_with_nutriguide([{"role": "user", "content": prompt}], max_tokens=600)


def optimize_shopping_ai(items_text: str, budget_level: str) -> str:
    """
    Get Claude's shopping list optimization suggestions.
    
    Args:
        items_text: Formatted string of shopping items
        budget_level: "low", "medium", or "high"
    """
    prompt = f"""Optimize this shopping list for a {budget_level} budget:

{items_text}

Please:
1. 🏭 Flag any ultra-processed items (UPF) and suggest a healthier swap
2. 💰 Suggest cheaper alternatives for expensive items
3. 💡 Give 3 practical tips specific to this list
4. 📊 Estimate potential weekly savings (as a $ range)

Keep it short and actionable."""

    return chat_with_nutriguide([{"role": "user", "content": prompt}], max_tokens=768)
