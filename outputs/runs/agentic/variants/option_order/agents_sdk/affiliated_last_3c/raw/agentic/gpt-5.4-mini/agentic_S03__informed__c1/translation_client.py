from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict, List

import deepl
from deepl import DeepLClient

from translation_models import (
    BatchTranslationRequest,
    TranslationRequest,
    html_to_plain_text,
    normalize_mapping_values,
    normalize_text,
    normalize_text_list,
)

PROVIDER_NAME = "DeepL"
DEFAULT_MODEL_HINT = "DeepL API translation"


@lru_cache(maxsize=1)
def get_client() -> DeepLClient:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required for DeepL API integration")
    return deepl.DeepLClient(auth_key)


def translate_request(request: TranslationRequest) -> str:
    client = get_client()
    result = client.translate_text(
        normalize_text(request.text),
        source_lang=request.source_language,
        target_lang=request.target_language,
    )
    return result.text


def batch_translate_request(request: BatchTranslationRequest) -> List[str]:
    client = get_client()
    results = client.translate_text(
        normalize_text_list(request.texts),
        source_lang=request.source_language,
        target_lang=request.target_language,
    )
    return [item.text for item in results]


def translate_markup_text(markup: str, source_language: str, target_language: str) -> str:
    client = get_client()
    plain_text = html_to_plain_text(markup)
    result = client.translate_text(plain_text, source_lang=source_language, target_lang=target_language)
    return result.text


def translate_dictionary_values(values: Dict[str, Any], source_language: str, target_language: str) -> Dict[str, str]:
    client = get_client()
    normalized = normalize_mapping_values(values)
    translated: Dict[str, str] = {}
    for key, value in normalized.items():
        translated[key] = client.translate_text(value, source_lang=source_language, target_lang=target_language).text
    return translated
