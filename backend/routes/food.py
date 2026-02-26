"""
/food routes — barcode scan using Open Food Facts (free, no API key needed).
"""

import httpx
from fastapi import APIRouter, HTTPException
from models.schemas import FoodScanRequest, FoodScanResponse
from core.config import OFF_BASE_URL
from core.ai_client import analyze_food_ai

router = APIRouter()


def compute_health_score(product: dict) -> float:
    """
    Compute a 0–10 health score from Open Food Facts data.
    Uses Nutri-Score + NOVA group as primary signals.
    """
    score = 5.0  # neutral baseline

    # Nutri-Score adjustment (A best, E worst)
    nutriscore = product.get("nutriscore_grade", "").lower()
    nutriscore_map = {"a": +3.0, "b": +1.5, "c": 0.0, "d": -1.5, "e": -3.0}
    score += nutriscore_map.get(nutriscore, 0.0)

    # NOVA group adjustment (1 = unprocessed, 4 = ultra-processed)
    try:
        nova = int(product.get("nova_group", 2))
        nova_map = {1: +2.0, 2: +1.0, 3: -0.5, 4: -2.0}
        score += nova_map.get(nova, 0.0)
    except (ValueError, TypeError):
        pass

    return round(min(max(score, 0.0), 10.0), 1)


@router.post("/scan", response_model=FoodScanResponse)
async def scan_food(request: FoodScanRequest):
    """
    Scan a food barcode → get nutrition data + AI health analysis.
    Uses Open Food Facts (completely free, no API key required).
    
    Try these real barcodes:
    - 3017620422003  (Nutella)
    - 5000159484763  (Kit Kat)
    - 0038000138690  (Kellogg's Corn Flakes)
    - 8710398525406  (Quaker Oats)
    """
    barcode = request.barcode.strip()

    # Call Open Food Facts
    url = f"{OFF_BASE_URL}/product/{barcode}.json"
    async with httpx.AsyncClient(timeout=10.0) as http:
        resp = await http.get(url)

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail="Could not reach Open Food Facts.")

    data = resp.json()

    if data.get("status") != 1:
        raise HTTPException(
            status_code=404,
            detail=f"Product with barcode {barcode} not found in Open Food Facts database.",
        )

    product = data.get("product", {})
    nutriments = product.get("nutriments", {})

    # Flatten key nutriment fields
    food_data = {
        "product_name":      product.get("product_name", "Unknown Product"),
        "brands":            product.get("brands", "Unknown Brand"),
        "ingredients_text":  product.get("ingredients_text", ""),
        "nutriscore_grade":  product.get("nutriscore_grade", "unknown"),
        "nova_group":        product.get("nova_group", "unknown"),
        "energy_kcal_100g":  nutriments.get("energy-kcal_100g"),
        "proteins_100g":     nutriments.get("proteins_100g"),
        "sugars_100g":       nutriments.get("sugars_100g"),
        "salt_100g":         nutriments.get("salt_100g"),
        "fat_100g":          nutriments.get("fat_100g"),
    }

    health_score = compute_health_score(product)

    # Get Claude's AI analysis
    try:
        ai_text = analyze_food_ai(food_data)
    except Exception:
        ai_text = "AI analysis temporarily unavailable. Please check your ANTHROPIC_API_KEY."

    # Parse alternatives from AI text (simple heuristic — Claude lists them)
    alternatives = []
    for line in ai_text.split("\n"):
        if "alternative" in line.lower() or "instead" in line.lower():
            alternatives.append(line.strip("- •1234567890.").strip())
            if len(alternatives) >= 2:
                break

    return FoodScanResponse(
        barcode=barcode,
        product_name=food_data["product_name"],
        brand=food_data["brands"],
        health_score=health_score,
        upf_level=int(product.get("nova_group", 2)) if str(product.get("nova_group", "")).isdigit() else 2,
        nutriscore=product.get("nutriscore_grade", "unknown").upper(),
        calories_100g=food_data["energy_kcal_100g"],
        protein_100g=food_data["proteins_100g"],
        sugar_100g=food_data["sugars_100g"],
        fat_100g=food_data["fat_100g"],
        ai_analysis=ai_text,
        alternatives=alternatives if alternatives else ["Whole food version", "Store-brand alternative"],
        image_url=product.get("image_front_url"),
    )
