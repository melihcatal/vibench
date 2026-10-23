from __future__ import annotations

import os
from typing import Iterable, List, Optional

import deepl

from translation_models import BatchTranslationResponse, TranslationRequest, TranslationResponse


DEEPL_ENV_KEY = "DEEPL_AUTH_KEY"
DEEPL_MODEL_TYPE = "quality_optimized"


class DeepLTranslationClient:
    def __init__(self, auth_key: Optional[str] = None) -> None:
        self.auth_key = auth_key or os.getenv(DEEPL_ENV_KEY)
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY is required")
        self.client = deepl.Translator(self.auth_key)

    def translate_text(self, request: TranslationRequest) -> TranslationResponse:
        result = self.client.translate_text(**request.to_deepl_payload())
        return TranslationResponse(
            text=result.text,
            detected_source_language=getattr(result, "detected_source_lang", None),
            billed_characters=getattr(result, "billed_characters", None),
            raw=result,
        )

    def translate_texts(self, requests: Iterable[TranslationRequest]) -> BatchTranslationResponse:
        prepared: List[TranslationRequest] = list(requests)
        if not prepared:
            raise ValueError("requests must not be empty")
        base = prepared[0]
        payload = {
            "text": [item.text for item in prepared],
            "target_lang": base.target_language,
            "preserve_formatting": base.preserve_formatting,
            "model_type": base.model_type or DEEPL_MODEL_TYPE,
        }
        if base.source_language:
            payload["source_lang"] = base.source_language
        if base.tag_handling:
            payload["tag_handling"] = base.tag_handling
        if base.formality:
            payload["formality"] = base.formality
        if base.context:
            payload["context"] = base.context
        results = self.client.translate_text(**payload)
        return BatchTranslationResponse(
            translations=[
                TranslationResponse(
                    text=item.text,
                    detected_source_language=getattr(item, "detected_source_lang", None),
                    billed_characters=getattr(item, "billed_characters", None),
                    raw=item,
                )
                for item in results
            ]
        )
