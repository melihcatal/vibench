from __future__ import annotations

from openai import OpenAI

TRANSLATION_MODEL = "gpt-4.1-mini"


def invoice_note_translate(text: str, target_language: str = "en") -> str:
    client = OpenAI()
    response = client.responses.create(
        model=TRANSLATION_MODEL,
        input=[
            {"role": "system", "content": f"Translate invoice notes into {target_language}."},
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
