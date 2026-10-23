from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI


def compliance_note_translate(note: str, target_language: str = "en") -> Dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Translate the following encryption or compliance note into {target_language}: {note}",
    )
    return {"model": "gpt-4.1-mini", "translated_text": response.output_text}
