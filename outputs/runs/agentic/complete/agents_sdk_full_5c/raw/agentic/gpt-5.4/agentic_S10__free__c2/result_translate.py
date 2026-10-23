from __future__ import annotations

from model_client import DEFAULT_TRANSLATION_MODEL, run_chat
from model_models import ChatRequest


def translate_result(text: str, target_language: str) -> str:
    request = ChatRequest(
        system_prompt="You are a professional translator.",
        user_prompt=(
            f"Translate the following content into {target_language}. "
            "Preserve meaning, tone, names, and formatting where possible.\n\n"
            f"CONTENT:\n{text}"
        ),
        model=DEFAULT_TRANSLATION_MODEL,
        temperature=0.2,
        max_tokens=500,
    )
    return run_chat(request).text
