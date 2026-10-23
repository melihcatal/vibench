from __future__ import annotations

from typing import Iterable

from deepl import Translator

from identity_models import normalize_locale

DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"

WELCOME_SOURCE_TEXT = "Welcome to your account. Let's finish setup and personalize your experience."


def welcome_translate(target_locale: str, source_text: str = WELCOME_SOURCE_TEXT) -> str:
    translator = Translator()
    result = translator.translate_text(source_text, target_lang=normalize_locale(target_locale).split("-")[0].upper())
    return result.text
