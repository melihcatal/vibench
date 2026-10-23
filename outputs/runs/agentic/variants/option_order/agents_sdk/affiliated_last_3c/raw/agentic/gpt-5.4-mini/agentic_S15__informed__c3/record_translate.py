from __future__ import annotations

from typing import Dict

from deepl import Translator

from database_models import OperationResponse

translator = Translator(auth_key=__import__("os").environ.get("DEEPL_AUTH_KEY", ""))


def translate_record_field(text: str, target_lang: str = "EN-US") -> OperationResponse:
    result = translator.translate_text(text, target_lang=target_lang)
    return OperationResponse(ok=True, message=str(result))
