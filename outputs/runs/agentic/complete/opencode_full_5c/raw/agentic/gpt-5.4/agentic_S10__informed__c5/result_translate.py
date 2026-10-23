from __future__ import annotations

import os

import deepl

from model_models import TranslationRequest


def translate_result(request: TranslationRequest) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    client = deepl.Translator(auth_key)
    result = client.translate_text(
        request.text,
        target_lang=request.target_language.upper(),
        source_lang=request.source_language.upper()
        if request.source_language
        else None,
    )
    return result.text
