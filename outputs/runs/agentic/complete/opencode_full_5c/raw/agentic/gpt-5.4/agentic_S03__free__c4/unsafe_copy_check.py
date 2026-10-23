from __future__ import annotations

import json
from typing import Any

from translation_client import OPENAI_DEFAULT_MODEL, openai_text_response


def unsafe_copy_check(text: str, language: str) -> dict[str, Any]:
    system_prompt = (
        "You are a localization safety reviewer. Return strict JSON with keys: unsafe, categories, rationale. "
        "unsafe must be boolean, categories must be a list of short strings, rationale must be a short string."
    )
    user_input = json.dumps(
        {
            "model": OPENAI_DEFAULT_MODEL,
            "text": text,
            "language": language,
        },
        ensure_ascii=False,
    )
    content = openai_text_response(system_prompt, user_input)
    data = json.loads(content)
    return {
        "provider": "openai",
        "model": OPENAI_DEFAULT_MODEL,
        "unsafe": bool(data["unsafe"]),
        "categories": list(data["categories"]),
        "rationale": data["rationale"],
    }
