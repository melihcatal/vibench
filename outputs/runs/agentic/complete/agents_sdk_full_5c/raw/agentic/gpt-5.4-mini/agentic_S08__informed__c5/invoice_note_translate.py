from __future__ import annotations

from typing import Dict

from openai import OpenAI

TRANSLATION_MODEL = "gpt-4o-mini"


def invoice_note_translate(text: str, target_language: str) -> Dict[str, str]:
    client = OpenAI()
    response = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": "Translate invoice notes accurately and preserve amounts, dates, and named entities."},
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
        temperature=0.1,
    )
    return {"provider": "openai", "model": TRANSLATION_MODEL, "translated_text": response.choices[0].message.content or ""}
