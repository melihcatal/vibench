from __future__ import annotations

import deepl


def translate_alt_text(text: str, target_language: str = "DE"):
    translator = deepl.Translator(auth_key=__import__("os").environ.get("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_language)
    return result.text
