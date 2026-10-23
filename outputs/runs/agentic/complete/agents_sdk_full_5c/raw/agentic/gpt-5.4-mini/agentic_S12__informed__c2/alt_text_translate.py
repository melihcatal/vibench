from __future__ import annotations

import os

from deepl import Translator


def translate_alt_text(text: str, target_lang: str = "DE"):
    translator = Translator(auth_key=os.getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_lang)
    return str(result)
