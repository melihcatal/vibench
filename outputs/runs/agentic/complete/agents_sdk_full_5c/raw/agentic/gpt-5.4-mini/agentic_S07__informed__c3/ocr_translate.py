from __future__ import annotations

from deepl import Translator

from document_models import TranslationResult


def translate_ocr_text(text: str, target_lang: str = "EN-US") -> TranslationResult:
    translator = Translator(auth_key=os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang)
    return TranslationResult(translated_text=getattr(result, "text", str(result)), provider="deepl", raw=result)


import os
