from __future__ import annotations

from model_client import create_text_response
from model_models import normalize_text_response, trim_text


def translate_result(
    text: str,
    target_language: str,
    source_language: str | None = None,
    model: str | None = None,
) -> dict:
    source_clause = f" from {source_language}" if source_language else ""
    response = create_text_response(
        system_prompt="You are a precise translation system that preserves meaning, names, and formatting.",
        user_prompt=f"Translate the following text{source_clause} to {target_language}. Return only the translated text.\n\nText:\n{trim_text(text, 12000)}",
        task_name="translation",
        model=model,
        temperature=0.1,
        max_output_tokens=500,
    )
    normalized = normalize_text_response(response)
    return normalized.__dict__
