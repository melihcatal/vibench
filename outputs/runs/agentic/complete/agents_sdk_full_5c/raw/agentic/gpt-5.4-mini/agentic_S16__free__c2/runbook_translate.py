from __future__ import annotations

import os

from openai import OpenAI

from security_models import TranslationRequest

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")
SOURCE_LANG = os.getenv("RUNBOOK_SOURCE_LANG", "en")
TARGET_LANG = os.getenv("RUNBOOK_TARGET_LANG", "es")


def translate_runbook_notes(text: str, source_lang: str = SOURCE_LANG, target_lang: str = TARGET_LANG) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    request = TranslationRequest(text=text, source_lang=source_lang, target_lang=target_lang)
    prompt = f"Translate the following secret-rotation runbook notes from {request.source_lang} to {request.target_lang}. Return only the translated text:\n\n{request.text}"
    response = client.chat.completions.create(model=TRANSLATION_MODEL, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content or ""
