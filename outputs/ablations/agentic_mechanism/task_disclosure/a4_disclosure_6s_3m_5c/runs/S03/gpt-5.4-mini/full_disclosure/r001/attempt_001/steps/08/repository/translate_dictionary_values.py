from __future__ import annotations

import os
from typing import Any, Dict, Mapping, Optional

from openai import OpenAI


def translate_dictionary_values(
    data: Mapping[str, Any],
    source_language: str,
    target_language: str,
    model: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if client is None:
        client = OpenAI(api_key=api_key)
    model_name = model or os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")

    translated: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, str):
            response = client.responses.create(
                model=model_name,
                input=[
                    {
                        "role": "system",
                        "content": "You are a professional translation engine. Translate only the provided text and preserve meaning.",
                    },
                    {
                        "role": "user",
                        "content": f"Translate from {source_language} to {target_language}: {value}",
                    },
                ],
            )
            translated[key] = response.output_text
        else:
            translated[key] = value
    return translated
