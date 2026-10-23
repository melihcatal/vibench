from __future__ import annotations

import os

from deepl import Translator


DEEPL_TARGET_DEFAULT = "EN-US"


def dashboard_note_translate(text: str, target_lang: str = DEEPL_TARGET_DEFAULT, source_lang: str | None = None) -> str:
    translator = Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return result.text
