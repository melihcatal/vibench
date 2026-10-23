import os
from typing import Optional
import deepl
from identity_models import TranslationResult


def translate_consent_text(
    text: str,
    target_language: str = "EN",
    source_language: Optional[str] = None,
    formality: str = "default",
) -> TranslationResult:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(auth_key)
    translate_options = {"target_lang": target_language}
    if source_language:
        translate_options["source_lang"] = source_language
    if formality != "default":
        translate_options["formality"] = formality
    result = translator.translate_text(text, **translate_options)
    detected_source = (
        result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else (source_language or "auto")
    )
    return TranslationResult(
        source_text=text,
        translated_text=result.text,
        source_language=detected_source,
        target_language=target_language,
    )


def translate_consent_batch(
    texts: list[str],
    target_language: str = "EN",
    source_language: Optional[str] = None,
    formality: str = "default",
) -> list[TranslationResult]:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(auth_key)
    translate_options = {"target_lang": target_language}
    if source_language:
        translate_options["source_lang"] = source_language
    if formality != "default":
        translate_options["formality"] = formality
    results = translator.translate_text(texts, **translate_options)
    if isinstance(results, list):
        return [
            TranslationResult(
                source_text=orig,
                translated_text=r.text,
                source_language=r.detected_source_lang
                if hasattr(r, "detected_source_lang")
                else (source_language or "auto"),
                target_language=target_language,
            )
            for orig, r in zip(texts, results)
        ]
    else:
        return [
            TranslationResult(
                source_text=texts[0],
                translated_text=results.text,
                source_language=results.detected_source_lang
                if hasattr(results, "detected_source_lang")
                else (source_language or "auto"),
                target_language=target_language,
            )
        ]


def translate_idp_consent_copy(
    consent_text: str,
    provider_name: str,
    target_languages: list[str],
    source_language: Optional[str] = None,
) -> dict:
    translations = {}
    for lang in target_languages:
        result = translate_consent_text(
            text=consent_text,
            target_language=lang,
            source_language=source_language,
        )
        translations[lang] = result.translated_text
    return {
        "provider": provider_name,
        "source_text": consent_text,
        "source_language": source_language or "auto",
        "translations": translations,
        "translation_service": "deepl",
    }


def get_supported_languages() -> list[dict]:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(auth_key)
    target_langs = translator.get_target_languages()
    source_langs = translator.get_source_languages()
    return {
        "target_languages": [
            {"code": lang.code, "name": lang.name} for lang in target_langs
        ],
        "source_languages": [
            {"code": lang.code, "name": lang.name} for lang in source_langs
        ],
        "provider": "deepl",
    }
