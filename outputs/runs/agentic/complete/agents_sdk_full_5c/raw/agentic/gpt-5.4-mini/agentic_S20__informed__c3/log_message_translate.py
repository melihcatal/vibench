from __future__ import annotations

import os

from deepl import Translator

from observability_models import TranslationResult


def translate_log_message(text: str, target_locale: str) -> TranslationResult:
    translator = Translator(auth_key=os.getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_locale.upper())
    return TranslationResult(text=str(result), target_locale=target_locale, raw_response=result)
