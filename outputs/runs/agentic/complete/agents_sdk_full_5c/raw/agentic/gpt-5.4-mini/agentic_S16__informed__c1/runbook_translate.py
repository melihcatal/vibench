from __future__ import annotations

import os

from openai import OpenAI


TRANSLATION_MODEL = os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def runbook_translate(text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    result = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": f"Translate the secret-rotation runbook into {target_language}."},
            {"role": "user", "content": text},
        ],
    )
    return result.choices[0].message.content or ""
