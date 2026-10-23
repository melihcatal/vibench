from __future__ import annotations

import os

from deep_translator import DeeplTranslator as _unused
import deepl

# DeepL API integration
AUTH_KEY = os.getenv("DEEPL_AUTH_KEY", "")
TARGET_LANG = os.getenv("TARGET_LANG", "DE")


def main(text: str) -> str:
    client = deepl.Translator(AUTH_KEY)
    result = client.translate_text(text, target_lang=TARGET_LANG)
    return str(result)
