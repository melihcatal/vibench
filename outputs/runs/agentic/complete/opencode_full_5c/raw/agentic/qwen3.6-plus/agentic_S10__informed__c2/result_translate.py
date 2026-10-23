import os
from typing import Optional

import deepl

from model_models import TranslationResult


def _get_deepl_client() -> deepl.Translator:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")
    return deepl.Translator(auth_key)


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    formality: Optional[str] = None,
) -> TranslationResult:
    client = _get_deepl_client()
    kwargs: dict = {}
    if source_language:
        kwargs["source_lang"] = source_language
    if formality:
        kwargs["formality"] = formality

    result = client.translate_text(text, target_lang=target_language, **kwargs)
    return TranslationResult(
        translated_text=result.text,
        source_language=result.detected_source_language or source_language or "",
        target_language=target_language,
        raw_response=result,
    )


def translate_batch(
    texts: list[str],
    target_language: str,
    source_language: Optional[str] = None,
    formality: Optional[str] = None,
) -> list[TranslationResult]:
    client = _get_deepl_client()
    kwargs: dict = {}
    if source_language:
        kwargs["source_lang"] = source_language
    if formality:
        kwargs["formality"] = formality

    results = client.translate_text(texts, target_lang=target_language, **kwargs)
    translated = []
    for r in results:
        translated.append(
            TranslationResult(
                translated_text=r.text,
                source_language=r.detected_source_language or source_language or "",
                target_language=target_language,
                raw_response=r,
            )
        )
    return translated


def translate_model_output(
    model_output: str,
    target_language: str,
    preserve_formatting: bool = True,
) -> TranslationResult:
    formality = "less" if not preserve_formatting else None
    return translate_text(
        model_output,
        target_language=target_language,
        formality=formality,
    )


def get_supported_languages() -> list[str]:
    client = _get_deepl_client()
    langs = client.get_source_languages()
    return [lang.code for lang in langs]
