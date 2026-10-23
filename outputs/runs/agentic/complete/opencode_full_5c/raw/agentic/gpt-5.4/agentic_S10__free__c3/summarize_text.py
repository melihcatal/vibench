from __future__ import annotations

from model_client import DEFAULT_CHAT_MODEL, build_chat_request, get_openai_client
from model_models import normalize_generation_response


def summarize_text(text: str, max_output_tokens: int = 220) -> dict:
    client = get_openai_client()
    request = build_chat_request(
        "Summarize the provided text into a concise, faithful summary with key points.",
        text,
        model=DEFAULT_CHAT_MODEL,
        temperature=0.2,
        max_output_tokens=max_output_tokens,
    )
    response = client.chat.completions.create(**request.to_openai())
    result = normalize_generation_response(response)
    return {"summary": result.text, "model": result.model, "usage": result.usage}
