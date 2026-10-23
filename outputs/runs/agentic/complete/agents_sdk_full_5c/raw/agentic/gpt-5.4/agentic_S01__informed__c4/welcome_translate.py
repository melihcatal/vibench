from __future__ import annotations

import os

import deepl

from identity_client import get_project_locale
from identity_models import TranslationResult


DEEPL_MODEL_TYPE = "prefer_quality_optimized"


def welcome_translate(copy_text: str, target_locale: str | None = None) -> TranslationResult:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    client = deepl.Translator(auth_key)
    locale = target_locale or get_project_locale()
    result = client.translate_text(copy_text, target_lang=locale.upper(), model_type=DEEPL_MODEL_TYPE)
    return TranslationResult(translated_text=result.text, target_locale=locale, provider="deepl")
