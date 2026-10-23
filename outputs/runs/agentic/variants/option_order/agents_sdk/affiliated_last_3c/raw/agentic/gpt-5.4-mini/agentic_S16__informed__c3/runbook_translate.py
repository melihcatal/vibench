from __future__ import annotations

from typing import List

from openai import OpenAI

OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


def runbook_translate(notes: str, target_language: str) -> str:
    client = OpenAI()
    messages: List[dict] = [
        {"role": "system", "content": "Translate secret-rotation runbook notes while preserving technical terms, identifiers, and code snippets."},
        {"role": "user", "content": f"Translate the following into {target_language}:\n{notes}"},
    ]
    response = client.chat.completions.create(model=OPENAI_TRANSLATION_MODEL, messages=messages)
    return response.choices[0].message.content or ""
