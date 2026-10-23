import os
from typing import Optional, List

import deepl

from security_models import TranslationResult

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_API_URL = os.environ.get("DEEPL_API_URL", "https://api.deepl.com")

DEFAULT_TARGET_LANGUAGE = "EN-US"
DEFAULT_SOURCE_LANGUAGE = "AUTO"


def get_deepl_client() -> deepl.Translator:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    return deepl.Translator(DEEPL_AUTH_KEY, server_url=DEEPL_API_URL)


def translate_compliance_note(
    text: str,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: str = DEFAULT_SOURCE_LANGUAGE,
) -> TranslationResult:
    translator = get_deepl_client()

    translate_kwargs = {
        "target_lang": target_language,
    }
    if source_language and source_language != DEFAULT_SOURCE_LANGUAGE:
        translate_kwargs["source_lang"] = source_language

    try:
        result = translator.translate_text(text, **translate_kwargs)
    except deepl.DeepLException as e:
        raise RuntimeError(f"DeepL translation request failed: {e}") from e

    return TranslationResult(
        translated_text=result.text,
        source_language=result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else source_language,
        target_language=target_language,
        model="deepl",
    )


def translate_compliance_notes_batch(
    texts: List[str],
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: str = DEFAULT_SOURCE_LANGUAGE,
) -> List[TranslationResult]:
    if not texts:
        return []

    translator = get_deepl_client()

    translate_kwargs = {
        "target_lang": target_language,
    }
    if source_language and source_language != DEFAULT_SOURCE_LANGUAGE:
        translate_kwargs["source_lang"] = source_language

    try:
        results = translator.translate_text(texts, **translate_kwargs)
    except deepl.DeepLException as e:
        raise RuntimeError(f"DeepL batch translation request failed: {e}") from e

    if isinstance(results, list):
        return [
            TranslationResult(
                translated_text=r.text,
                source_language=r.detected_source_lang
                if hasattr(r, "detected_source_lang")
                else source_language,
                target_language=target_language,
                model="deepl",
            )
            for r in results
        ]
    else:
        return [
            TranslationResult(
                translated_text=results.text,
                source_language=results.detected_source_lang
                if hasattr(results, "detected_source_lang")
                else source_language,
                target_language=target_language,
                model="deepl",
            )
        ]


def translate_to_english(
    text: str,
) -> TranslationResult:
    return translate_compliance_note(
        text=text,
        target_language="EN-US",
    )


def translate_to_reviewer_language(
    text: str,
    reviewer_language: str = "EN-US",
) -> TranslationResult:
    return translate_compliance_note(
        text=text,
        target_language=reviewer_language,
    )
