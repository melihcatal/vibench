from typing import List, Dict, Optional
import os
import deepl
from translation_models import TranslationRequest, TranslationResponse


class DeepLTranslationClient:
    def __init__(self, auth_key: Optional[str] = None):
        self.auth_key = auth_key or os.getenv("DEEPL_AUTH_KEY")
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable not set")
        self.translator = deepl.Translator(self.auth_key)

    def translate_text(self, request: TranslationRequest) -> TranslationResponse:
        result = self.translator.translate_text(
            request.text,
            target_lang=request.target_language,
            source_lang=request.source_language if request.source_language else None,
            preserve_formatting=True,
        )
        return TranslationResponse(
            translated_text=result.text,
            detected_source_language=result.detected_source_lang,
        )
