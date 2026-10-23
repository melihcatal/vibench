import os
from typing import List, Optional

import deepl

from identity_models import TranslationResult


DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY", "")


def create_deepl_client() -> deepl.Translator:
    return deepl.Translator(DEEPL_AUTH_KEY)


def translate_consent_text(
    source_text: str,
    target_language: str,
    source_language: Optional[str] = None,
    formality: Optional[str] = None,
) -> TranslationResult:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    client = create_deepl_client()

    translate_kwargs = {
        "target_lang": target_language.upper(),
    }
    if source_language:
        translate_kwargs["source_lang"] = source_language.upper()
    if formality:
        translate_kwargs["formality"] = formality

    result = client.translate_text(
        source_text,
        **translate_kwargs,
    )

    return TranslationResult(
        source_text=source_text,
        translated_text=result.text,
        source_language=result.detected_source_lang or source_language or "",
        target_language=target_language,
        provider="deepl",
    )


def translate_consent_batch(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
    formality: Optional[str] = None,
) -> List[TranslationResult]:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    client = create_deepl_client()

    translate_kwargs = {
        "target_lang": target_language.upper(),
    }
    if source_language:
        translate_kwargs["source_lang"] = source_language.upper()
    if formality:
        translate_kwargs["formality"] = formality

    results = client.translate_text(
        texts,
        **translate_kwargs,
    )

    translation_results = []
    for i, result in enumerate(results):
        translation_results.append(
            TranslationResult(
                source_text=texts[i],
                translated_text=result.text,
                source_language=result.detected_source_lang or source_language or "",
                target_language=target_language,
                provider="deepl",
            )
        )

    return translation_results


def translate_idp_consent_copy(
    provider_name: str,
    consent_text: str,
    target_languages: List[str],
    source_language: Optional[str] = None,
    formality: Optional[str] = None,
) -> dict:
    translations = {}
    for lang in target_languages:
        result = translate_consent_text(
            source_text=consent_text,
            target_language=lang,
            source_language=source_language,
            formality=formality,
        )
        translations[lang] = result.translated_text

    return {
        "provider": provider_name,
        "source_language": translations.get(
            "source_language", source_language or "auto"
        ),
        "consent_text": consent_text,
        "translations": translations,
        "translation_service": "deepl",
    }


def get_supported_languages() -> dict:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    client = create_deepl_client()
    source_languages = client.get_source_languages()
    target_languages = client.get_target_languages()

    return {
        "source_languages": [
            {"code": lang.code, "name": lang.name} for lang in source_languages
        ],
        "target_languages": [
            {
                "code": lang.code,
                "name": lang.name,
                "supports_formality": lang.supports_formality,
            }
            for lang in target_languages
        ],
        "provider": "deepl",
    }
