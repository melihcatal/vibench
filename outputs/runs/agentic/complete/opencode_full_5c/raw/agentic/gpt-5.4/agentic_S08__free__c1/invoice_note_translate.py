from __future__ import annotations

import os

from openai import OpenAI


OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def invoice_note_translate(text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_TRANSLATION_MODEL,
        input=[
            {
                "role": "system",
                "content": f"Translate invoice notes into {target_language} while preserving amounts, dates, and vendor-specific terminology.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
