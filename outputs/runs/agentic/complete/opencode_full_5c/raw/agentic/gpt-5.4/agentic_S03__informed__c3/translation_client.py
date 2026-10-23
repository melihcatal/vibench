from __future__ import annotations

import os
from typing import Iterable, List

import deepl

from translation_models import (
    TranslationRequest,
    TranslationResult,
    normalize_language_code,
    normalize_texts,
)


def get_deepl_client() -> deepl.Translator:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    server_url = os.environ.get("DEEPL_SERVER_URL")
    if server_url:
        return deepl.Translator(auth_key, server_url=server_url)
    return deepl.Translator(auth_key)


def _translate_options(
    source_language: str | None, formality: str | None, preserve_formatting: bool
) -> dict:
    options = {
        "preserve_formatting": preserve_formatting,
    }
    normalized_source = normalize_language_code(source_language)
    if normalized_source:
        options["source_lang"] = normalized_source
    if formality:
        options["formality"] = formality
    return options


def translate_text_with_deepl(request: TranslationRequest) -> TranslationResult:
    client = get_deepl_client()
    result = client.translate_text(
        request.text,
        target_lang=normalize_language_code(request.target_language),
        **_translate_options(
            request.source_language, request.formality, request.preserve_formatting
        ),
    )
    return TranslationResult(
        text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", None),
        billed_characters=getattr(result, "billed_characters", None),
        raw=result,
    )


def translate_texts_with_deepl(
    texts: Iterable[str],
    source_language: str | None,
    target_language: str,
    formality: str | None = None,
    preserve_formatting: bool = True,
    tag_handling: str | None = None,
) -> List[TranslationResult]:
    normalized_text_list = normalize_texts(list(texts))
    if not normalized_text_list:
        return []
    client = get_deepl_client()
    options = _translate_options(source_language, formality, preserve_formatting)
    if tag_handling:
        options["tag_handling"] = tag_handling
    results = client.translate_text(
        normalized_text_list,
        target_lang=normalize_language_code(target_language),
        **options,
    )
    if not isinstance(results, list):
        results = [results]
    return [
        TranslationResult(
            text=item.text,
            detected_source_language=getattr(item, "detected_source_lang", None),
            billed_characters=getattr(item, "billed_characters", None),
            raw=item,
        )
        for item in results
    ]
