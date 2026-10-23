from __future__ import annotations

import os
from dataclasses import dataclass

from openai import OpenAI

TRANSLATE_MODEL = os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-4.1-mini")


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str


def translate_payload_text(text: str, target_language: str = "en") -> TranslationResult:
    client = OpenAI()
    response = client.responses.create(
        model=TRANSLATE_MODEL,
        input=[
            {"role": "system", "content": "Translate customer-facing text faithfully and concisely."},
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
    )
    translated = response.output_text
    return TranslationResult(translated_text=translated, source_language="auto", target_language=target_language)
