from __future__ import annotations

import os

import deepl


def localized_platform_output(text: str, target_lang: str, source_lang: str | None = None) -> str:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return result.text
