from __future__ import annotations

import os

from openai import OpenAI


OPENAI_TRANSLATE_MODEL = os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-4o-mini")


def multilingual_query_translate(query: str, target_language: str = "English") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_TRANSLATE_MODEL,
        input=[
            {
                "role": "system",
                "content": "Translate search queries accurately and keep product names, codes, and quoted phrases unchanged when possible.",
            },
            {
                "role": "user",
                "content": f"Translate this search query into {target_language}: {query}",
            },
        ],
    )
    return response.output_text.strip()
