from __future__ import annotations

import os

from openai import OpenAI


def compliance_note_translate(note: str, target_language: str = "en") -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Translate this encryption or compliance note into {target_language}: {note}"
    result = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return {"provider": "openai", "model": "gpt-5.4-mini", "translated_text": result.output_text}
