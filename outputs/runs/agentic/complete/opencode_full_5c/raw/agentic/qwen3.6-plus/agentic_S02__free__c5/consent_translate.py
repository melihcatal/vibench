import os
from typing import Optional
from datetime import datetime, timezone

import deepl

from identity_models import TranslationResult


PROVIDER = "deepl"
DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY", "")
DEEPL_API_URL = os.environ.get("DEEPL_API_URL", "https://api.deepl.com")
DEFAULT_TARGET_LANGUAGE = os.environ.get("DEEPL_DEFAULT_TARGET_LANG", "EN")


def get_deepl_client() -> deepl.Translator:
    return deepl.Translator(
        DEEPL_API_KEY,
        server_url=DEEPL_API_URL,
    )


def translate_consent_text(
    text: str,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: Optional[str] = None,
    client: Optional[deepl.Translator] = None,
) -> TranslationResult:
    deepl_client = client or get_deepl_client()
    result = deepl_client.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
        formality="more"
        if target_language in ("DE", "FR", "ES", "IT", "PT", "NL")
        else "default",
    )
    return TranslationResult(
        source_text=text,
        translated_text=result.text,
        source_language=result.detected_source_lang or source_language or "unknown",
        target_language=target_language,
        provider=PROVIDER,
    )


def translate_consent_batch(
    texts: list[str],
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: Optional[str] = None,
    client: Optional[deepl.Translator] = None,
) -> list[TranslationResult]:
    deepl_client = client or get_deepl_client()
    results = deepl_client.translate_text(
        texts,
        target_lang=target_language,
        source_lang=source_language,
        formality="more"
        if target_language in ("DE", "FR", "ES", "IT", "PT", "NL")
        else "default",
    )
    translations = []
    for i, result in enumerate(results):
        translations.append(
            TranslationResult(
                source_text=texts[i],
                translated_text=result.text,
                source_language=result.detected_source_lang
                or source_language
                or "unknown",
                target_language=target_language,
                provider=PROVIDER,
            )
        )
    return translations


def localize_consent_form(
    form_fields: dict[str, str],
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    client: Optional[deepl.Translator] = None,
) -> dict:
    deepl_client = client or get_deepl_client()
    texts_to_translate = list(form_fields.values())
    if not texts_to_translate:
        return form_fields
    results = deepl_client.translate_text(
        texts_to_translate,
        target_lang=target_language,
        formality="more"
        if target_language in ("DE", "FR", "ES", "IT", "PT", "NL")
        else "default",
    )
    localized = {}
    for i, (key, _) in enumerate(form_fields.items()):
        localized[key] = results[i].text
    return localized


def get_supported_languages(
    client: Optional[deepl.Translator] = None,
) -> list[dict]:
    deepl_client = client or get_deepl_client()
    source_languages = deepl_client.get_source_languages()
    target_languages = deepl_client.get_target_languages()
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
    }


def translate_and_record(
    text: str,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: Optional[str] = None,
    user_id: Optional[str] = None,
    client: Optional[deepl.Translator] = None,
) -> dict:
    translation = translate_consent_text(
        text=text,
        target_language=target_language,
        source_language=source_language,
        client=client,
    )
    return {
        "translation": translation.to_dict(),
        "user_id": user_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": PROVIDER,
    }
