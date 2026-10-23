from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


def translate_query(query: str, target_language: str = "English", model: str = "gpt-4o-mini") -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required.")
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": f"Translate search queries into {target_language}. Return only the translation.",
            },
            {"role": "user", "content": query},
        ],
    )
    return {
        "provider": "OpenAI",
        "model": model,
        "translated_text": response.output_text,
    }
