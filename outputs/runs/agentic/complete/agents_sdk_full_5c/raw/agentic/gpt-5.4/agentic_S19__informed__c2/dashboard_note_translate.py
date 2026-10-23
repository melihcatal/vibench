from __future__ import annotations

import os

import deepl


TARGET_FORMALITY = "prefer_more"


def dashboard_note_translate(text: str, target_lang: str, source_lang: str | None = None) -> str:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        source_lang=source_lang,
        target_lang=target_lang,
        formality=TARGET_FORMALITY,
    )
    return result.text
