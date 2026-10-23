from __future__ import annotations

from deepl import Translator

from model_models import TranslationRequest

PROVIDER = "deepl"


def translate_result(text: str, target_language: str, source_language: str | None = None, model: str | None = None) -> str:
    req = TranslationRequest(text=text, target_language=target_language, source_language=source_language, model=model)
    translator = Translator(auth_key=os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(req.text, target_lang=req.target_language.upper(), source_lang=req.source_language.upper() if req.source_language else None)
    return result.text


import os
