from __future__ import annotations

import os
from typing import Iterable, List, Optional

import deepl

from translation_models import BatchTranslationRequest, TranslationRequest, TranslationResult, normalize_language_code


DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"
DEEPL_SERVER_URL_ENV = "DEEPL_SERVER_URL"
DEFAULT_PROVIDER = "DeepL API"


class DeepLTranslationClient:
    def __init__(self, auth_key: Optional[str] = None, server_url: Optional[str] = None) -> None:
        resolved_key = auth_key or os.getenv(DEEPL_AUTH_KEY_ENV)
        if not resolved_key:
            raise ValueError("Missing DeepL auth key. Set DEEPL_AUTH_KEY.")
        self._translator = deepl.Translator(
            auth_key=resolved_key,
            server_url=server_url or os.getenv(DEEPL_SERVER_URL_ENV),
        )

    @property
    def translator(self) -> deepl.Translator:
        return self._translator

    def translate_text(self, request: TranslationRequest) -> TranslationResult:
        response = self._translator.translate_text(**request.as_deepl_kwargs())
        return TranslationResult(
            text=response.text,
            detected_source_language=getattr(response, "detected_source_lang", None),
            billed_characters=getattr(response, "billed_characters", None),
            provider=DEFAULT_PROVIDER,
            raw={
                "target_lang": normalize_language_code(request.target_language),
                "source_lang": normalize_language_code(request.source_language),
                "model_type_used": getattr(response, "model_type_used", None),
            },
        )

    def translate_batch(self, request: BatchTranslationRequest) -> List[TranslationResult]:
        responses = self._translator.translate_text(
            text=list(request.texts),
            target_lang=normalize_language_code(request.target_language),
            source_lang=normalize_language_code(request.source_language),
            tag_handling="html" if request.text_type == "html" else None,
            preserve_formatting=request.preserve_formatting,
        )
        if not isinstance(responses, list):
            responses = [responses]
        return [
            TranslationResult(
                text=item.text,
                detected_source_language=getattr(item, "detected_source_lang", None),
                billed_characters=getattr(item, "billed_characters", None),
                provider=DEFAULT_PROVIDER,
                raw={"index": idx},
            )
            for idx, item in enumerate(responses)
        ]


def get_translation_client() -> DeepLTranslationClient:
    return DeepLTranslationClient()


def ensure_non_empty_texts(texts: Iterable[str]) -> List[str]:
    normalized = [str(text) for text in texts]
    if not normalized:
        raise ValueError("At least one text value is required.")
    return normalized
