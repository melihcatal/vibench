from __future__ import annotations

import os

from openai import OpenAI

from security_models import TranslationResult

OPENAI_TRANSLATION_MODEL = "gpt-4.1-mini"


def translate_runbook_notes(text: str, target_language: str = "es") -> TranslationResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=OPENAI_TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": f"Translate the following secret-rotation runbook notes into {target_language}."},
            {"role": "user", "content": text},
        ],
        temperature=0.1,
    )
    translated = response.choices[0].message.content or ""
    return TranslationResult(source_text=text, translated_text=translated, target_language=target_language)
