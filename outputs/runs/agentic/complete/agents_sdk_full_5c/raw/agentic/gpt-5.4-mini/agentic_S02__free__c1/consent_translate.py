from __future__ import annotations

import os

from openai import OpenAI

OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


def translate_consent_copy(text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=OPENAI_TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": f"Translate identity-provider consent copy into {target_language}."},
            {"role": "user", "content": text},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content or ""
