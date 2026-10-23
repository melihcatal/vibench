from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

PROVIDER_NAME = "openai"
MODEL_ID = "gpt-4o-mini"


def translate_invoice_note(note: str, target_language: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": f"Translate invoice notes into {target_language}. Preserve amounts and proper nouns."},
            {"role": "user", "content": note},
        ],
        temperature=0.1,
    )
    return {"provider": PROVIDER_NAME, "model": MODEL_ID, "translation": response.choices[0].message.content or ""}
