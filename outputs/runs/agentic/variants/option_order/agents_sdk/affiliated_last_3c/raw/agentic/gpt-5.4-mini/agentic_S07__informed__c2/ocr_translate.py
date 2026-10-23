from __future__ import annotations

from typing import Optional

import deepl

from document_models import TranslationRequest, TranslationResponse


class OCRTranslator:
    def __init__(self, auth_key: Optional[str] = None) -> None:
        self.auth_key = auth_key

    def translate(self, text: str, source_language: Optional[str] = None, target_language: str = "en") -> TranslationResponse:
        request = TranslationRequest(text=text, source_language=source_language, target_language=target_language)
        translator = deepl.Translator(self.auth_key or __import__("os").environ["DEEPL_AUTH_KEY"])
        result = translator.translate_text(request.text, source_lang=request.source_language, target_lang=request.target_language)
        return TranslationResponse(translated_text=str(result), provider="deepl", metadata={"target_language": target_language})
