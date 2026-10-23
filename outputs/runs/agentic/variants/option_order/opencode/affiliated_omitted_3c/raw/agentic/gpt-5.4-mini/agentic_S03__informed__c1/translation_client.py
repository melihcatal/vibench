import os
from typing import Any, Dict, List

import deepl

from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    TranslationRequest,
    TranslationResponse,
    normalize_mapping_values,
    normalize_text,
    normalize_texts,
)

_PROVIDER = "DeepL API"


def get_client() -> deepl.Translator:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    return deepl.Translator(auth_key)


def translate_request(request: TranslationRequest) -> TranslationResponse:
    client = get_client()
    result = client.translate_text(
        normalize_text(request.text),
        target_lang=request.target_language.upper(),
        source_lang=request.source_language.upper(),
        preserve_formatting=request.preserve_formatting,
    )
    return TranslationResponse(
        translated_text=result.text,
        source_language=request.source_language,
        target_language=request.target_language,
        provider=_PROVIDER,
        raw={"detected_source_language": getattr(result, "detected_source_lang", None)},
    )


def translate_texts(texts: List[str], source_language: str, target_language: str) -> BatchTranslationResponse:
    client = get_client()
    normalized = normalize_texts(texts)
    results = client.translate_text(
        normalized,
        target_lang=target_language.upper(),
        source_lang=source_language.upper(),
    )
    translated = [item.text for item in results]
    return BatchTranslationResponse(
        translated_texts=translated,
        source_language=source_language,
        target_language=target_language,
        provider=_PROVIDER,
        raw={"count": len(translated)},
    )


def translate_values(values: Dict[str, str], source_language: str, target_language: str) -> Dict[str, str]:
    translated = translate_texts(list(normalize_mapping_values(values).values()), source_language, target_language)
    return {key: text for key, text in zip(values.keys(), translated.translated_texts)}
