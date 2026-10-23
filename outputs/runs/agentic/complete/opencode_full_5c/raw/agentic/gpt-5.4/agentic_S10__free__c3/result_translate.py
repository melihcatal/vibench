from __future__ import annotations

from model_client import (
    DEFAULT_TRANSLATION_MODEL,
    build_chat_request,
    get_openai_client,
)
from model_models import normalize_generation_response


def translate_result(text: str, target_language: str) -> dict:
    client = get_openai_client()
    request = build_chat_request(
        f"Translate the user's text into {target_language} while preserving meaning and tone.",
        text,
        model=DEFAULT_TRANSLATION_MODEL,
        temperature=0.1,
        max_output_tokens=500,
    )
    response = client.chat.completions.create(**request.to_openai())
    result = normalize_generation_response(response)
    return {
        "translation": result.text,
        "target_language": target_language,
        "model": result.model,
    }
