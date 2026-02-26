"""
POST /ai/chat — Conversational NutriGuide AI.

Send a conversation history and get a contextual, personalized response.
"""

from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from core.ai_client import chat_with_nutriguide

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with NutriGuide AI",
    description=(
        "Free-form conversation with NutriGuide. "
        "Send a list of messages (your full conversation history) and get a response.\n\n"
        "**Example questions:**\n"
        "- Is oat milk healthier than dairy milk?\n"
        "- What can I cook with eggs, spinach, and leftover rice?\n"
        "- How can I eat well on $50 a week?\n"
        "- What does ultra-processed food mean?"
    ),
)
async def ai_chat(request: ChatRequest):
    if not request.messages:
        raise HTTPException(status_code=400, detail="messages list cannot be empty.")

    # Build messages for Claude
    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    # Inject user context into the first message if provided
    if request.user_context and messages:
        ctx = request.user_context
        context_str = (
            f"\n\n[User context — Goal: {ctx.get('goal', 'unknown')}, "
            f"Budget: {ctx.get('budget_level', 'unknown')}, "
            f"Allergies: {', '.join(ctx.get('allergies', [])) or 'none'}]"
        )
        messages[0]["content"] += context_str

    try:
        reply = chat_with_nutriguide(messages, max_tokens=1024)
    except ValueError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI chat failed: {str(e)}",
        )

    return ChatResponse(reply=reply, model_used="claude-haiku-4-5")
