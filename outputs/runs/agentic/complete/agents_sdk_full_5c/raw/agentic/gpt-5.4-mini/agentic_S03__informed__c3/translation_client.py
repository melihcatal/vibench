from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

import deepl

from translation_models import (
    BatchTranslationRequest,
    DictionaryTranslationRequest,
    MarkupTranslationRequest,
    TranslationRequest,
    ensure_string_mapping,
    normalize_whitespace,
)


@dataclass(frozen=True)
class TranslationConfig:
    auth_key: str
    provider: str = "deepl"
    api_host: str | None = None


class TranslationClient:
    def __init__(self, config: TranslationConfig | None = None):
        config = config or load_config()
        self.config = config
        kwargs: Dict[str, Any] = {}
        if config.api_host:
            kwargs["server_url"] = config.api_host
        self._client = deepl.Translator(config.auth_key, **kwargs)

    def translate_text(self, request: TranslationRequest) -> str:
        result = self._client.translate_text(
            normalize_whitespace(request.text),
            source_lang=request.source_language,
            target_lang=request.target_language,
        )
        return result.text

    def translate_batch(self, request: BatchTranslationRequest) -> List[str]:
        results = self._client.translate_text(
            [normalize_whitespace(text) for text in request.texts],
            source_lang=request.source_language,
            target_lang=request.target_language,
        )
        return [item.text for item in results]

    def translate_markup(self, request: MarkupTranslationRequest) -> str:
        result = self._client.translate_text(
            request.markup,
            source_lang=request.source_language,
            target_lang=request.target_language,
            tag_handling=request.format_type,
        )
        return result.text

    def translate_dictionary_values(self, request: DictionaryTranslationRequest) -> Dict[str, str]:
        values = ensure_string_mapping(request.values)
        translated = self._client.translate_text(
            list(values.values()),
            source_lang=request.source_language,
            target_lang=request.target_language,
        )
        return {key: item.text for key, item in zip(values.keys(), translated)}


def load_config() -> TranslationConfig:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    api_host = os.getenv("DEEPL_API_HOST")
    return TranslationConfig(auth_key=auth_key, api_host=api_host)
