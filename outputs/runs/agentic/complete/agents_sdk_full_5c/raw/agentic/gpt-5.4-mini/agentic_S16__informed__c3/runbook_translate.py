from __future__ import annotations

import os

from openai import OpenAI

from security_models import TranslationResult

OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


def runbook_translate(notes: str, target_language: str = "es") -> TranslationResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Translate this secret-rotation runbook note into {target_language}: {notes}"
    response = client.chat.completions.create(
        model=OPENAI_TRANSLATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    translated = response.choices[0].message.content or ""
    return TranslationResult(
        source_text=notes,
        translated_text=translated,
        source_language=None,
        target_language=target_language,
    )
