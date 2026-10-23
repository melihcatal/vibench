from __future__ import annotations

from typing import List

from openai import OpenAI


def translate_runbook_notes(notes: str, target_language: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate secret rotation runbook notes accurately."},
            {"role": "user", "content": f"Translate to {target_language}: {notes}"},
        ],
    )
    return response.choices[0].message.content or ""
