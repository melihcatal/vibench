from __future__ import annotations

import os
from typing import Iterable, List

import deepl

from translation_models import TranslationRequest, TranslationResult


DEEPL_MODEL_TYPE = os.getenv("DEEPL_MODEL_TYPE", "quality_optimized")


class DeepLTranslationClient:
    def __init__(self, auth_key: str | None = None) -> None:
        self.auth_key = auth_key or os.getenv("DEEPL_AUTH_KEY")
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY is required")
        self.translator = deepl.Translator(self.auth_key)

    def translate(self, request: TranslationRequest) -> TranslationResult:
        options = request.to_deepl_options()
        if "model_type" not in options:
            options["model_type"] = DEEPL_MODEL_TYPE
        response = self.translator.translate_text(request.text, **options)
        billed = getattr(response, "billed_characters", None)
        return TranslationResult(
            text=response.text,
            detected_source_language=getattr(response, "detected_source_lang", None),
            billed_characters=billed,
            provider="DeepL",
            model=options.get("model_type"),
            raw=response,
        )

    def translate_batch(self, requests: Iterable[TranslationRequest]) -> List[TranslationResult]:
        request_list = list(requests)
        if not request_list:
            return []
        first = request_list[0]
        options = first.to_deepl_options()
        if "model_type" not in options:
            options["model_type"] = DEEPL_MODEL_TYPE
        texts = [item.text for item in request_list]
        responses = self.translator.translate_text(texts, **options)
        return [
            TranslationResult(
                text=item.text,
                detected_source_language=getattr(item, "detected_source_lang", None),
                billed_characters=getattr(item, "billed_characters", None),
                provider="DeepL",
                model=options.get("model_type"),
                raw=item,
            )
            for item in responses
        ]


def get_translation_client() -> DeepLTranslationClient:
    return DeepLTranslationClient()
