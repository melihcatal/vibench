from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"


def invoice_note_translate(text: str, target_language: str = "en") -> Dict[str, Any]:
    client = OpenAI()
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": f"Translate invoice notes to {target_language}."},
            {"role": "user", "content": text},
        ],
        temperature=0.1,
    )
    return {"provider": "openai", "model": MODEL_ID, "translation": completion.choices[0].message.content or ""}
