from __future__ import annotations

import os

from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"


def translate_consent_copy(text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Translate identity-provider consent copy accurately and clearly."},
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
    )
    return result.choices[0].message.content or ""
