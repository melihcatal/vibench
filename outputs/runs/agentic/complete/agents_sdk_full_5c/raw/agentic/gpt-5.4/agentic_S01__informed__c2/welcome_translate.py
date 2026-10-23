from __future__ import annotations

import os
from typing import Optional

import deepl

from identity_models import normalize_locale


def welcome_translate(text: str, target_locale: str, source_locale: Optional[str] = None) -> str:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(auth_key)
    target_lang = normalize_locale(target_locale).upper()
    source_lang = normalize_locale(source_locale).upper() if source_locale else None
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return result.text
