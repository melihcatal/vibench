from __future__ import annotations

import os

from deep_translator import DeeplTranslator

from identity_models import TranslationRequest


def welcome_translate(text: str, locale: str, source_locale: str = "en"):
    req = TranslationRequest(text=text, locale=locale, source_locale=source_locale).normalized()
    translator = DeeplTranslator(api_key=os.getenv("DEEPL_AUTH_KEY", ""), source=req.source_locale, target=req.locale)
    return {"translated_text": translator.translate(req.text), "provider": "DeepL API"}
