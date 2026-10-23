from __future__ import annotations

from model_client import choose_model, generate_text
from model_models import ChatTurn, GenerationRequest


def summarize_text(text: str, model: str | None = None) -> dict:
    request = GenerationRequest(
        instructions="Summarize the input text into a concise overview with key points and notable risks or decisions.",
        input_text=text,
        model=choose_model("summarize", model),
        temperature=0.2,
        max_output_tokens=350,
    )
    result = generate_text(
        [
            ChatTurn(role="system", content=request.system_prompt()),
            ChatTurn(role="user", content=request.user_prompt()),
        ],
        model=request.model,
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
    )
    return {
        "provider": "openai",
        "model": result.model,
        "summary": result.text,
        "usage": result.usage,
    }
