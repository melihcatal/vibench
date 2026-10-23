from __future__ import annotations

from typing import Iterable

from openai import OpenAI


TRANSLATION_MODEL = "gpt-4o-mini"


def translate_runbook_notes(notes: Iterable[str], target_language: str) -> str:
    client = OpenAI()
    joined = "\n".join(notes)
    response = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": "Translate operational runbook notes accurately and preserve bullet structure."},
            {"role": "user", "content": f"Translate to {target_language}:\n{joined}"},
        ],
    )
    return response.choices[0].message.content or ""
