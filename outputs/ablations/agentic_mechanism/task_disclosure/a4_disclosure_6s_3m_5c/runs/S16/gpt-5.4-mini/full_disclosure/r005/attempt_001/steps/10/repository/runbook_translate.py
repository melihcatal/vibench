from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class RunbookTranslation:
    source_text: str
    translated_text: str
    target_language: str
    provider: str = "openai"
    model: str = "gpt-5.4-mini"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def translate_runbook_notes(notes: str, target_language: Optional[str] = None) -> RunbookTranslation:
    language = target_language or os.environ.get("TARGET_LANGUAGE", "English")
    client = _client()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Translate secret-rotation runbook notes accurately and preserve operational meaning.",
            },
            {
                "role": "user",
                "content": f"Translate the following runbook notes into {language}:\n\n{notes}",
            },
        ],
    )
    translated_text = response.output_text
    return RunbookTranslation(source_text=notes, translated_text=translated_text, target_language=language)
