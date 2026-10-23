from __future__ import annotations

import os
from typing import List

import deepl

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY", "")


def welcome_translate(text: str, target_locale: str) -> str:
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_locale.split("-")[0].upper())
    return result.text
