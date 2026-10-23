from __future__ import annotations

import os

import deepl

from document_models import OCRTextResponse, normalize_text

PROVIDER = "DeepL API"
MODEL_SIGNAL = "deepl"


def translate_ocr_text(text: str, target_lang: str = "EN-US") -> OCRTextResponse:
    client = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    translated = client.translate_text(normalize_text(text), target_lang=target_lang)
    return OCRTextResponse(text=normalize_text(getattr(translated, "text", translated)), raw=translated)
