"""Translate identity-provider consent copy using DeepL API."""

import os
from typing import Optional, Dict, Any, List

import deepl

from identity_models import UserProfileClaims


def translate_consent_text(
    text: str,
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate identity-provider consent copy using DeepL API.
    """
    translator = deepl.Translator(
        auth_key or os.environ.get("DEEPL_AUTH_KEY", ""),
    )

    kwargs: Dict[str, Any] = {}
    if source_lang:
        kwargs["source_lang"] = source_lang

    result = translator.translate_text(text, target_lang=target_lang, **kwargs)

    return {
        "translated_text": result.text,
        "detected_source_lang": result.detected_source_lang,
        "target_lang": target_lang,
        "provider": "DeepL",
        "original_text": text,
    }


def translate_consent_batch(
    texts: List[str],
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a batch of consent strings using DeepL API.
    """
    translator = deepl.Translator(
        auth_key or os.environ.get("DEEPL_AUTH_KEY", ""),
    )

    kwargs: Dict[str, Any] = {}
    if source_lang:
        kwargs["source_lang"] = source_lang

    results = translator.translate_text(texts, target_lang=target_lang, **kwargs)

    translations = []
    for original, translated in zip(texts, results):
        translations.append({
            "original": original,
            "translated": translated.text,
        })

    return {
        "translations": translations,
        "target_lang": target_lang,
        "detected_source_lang": results[0].detected_source_lang if results else None,
        "count": len(translations),
        "provider": "DeepL",
    }


def translate_consent_for_user(
    user: UserProfileClaims,
    consent_text: str,
    auth_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate consent text into the user's preferred locale using DeepL.
    Maps common locale codes to DeepL language codes.
    """
    locale_to_deepl = {
        "es": "ES",
        "fr": "FR",
        "de": "DE",
        "pt": "PT",
        "it": "IT",
        "nl": "NL",
        "pl": "PL",
        "ru": "RU",
        "ja": "JA",
        "zh": "ZH",
        "ko": "KO",
    }

    target = "EN"
    if user.locale:
        lang_code = user.locale.lower()[:2]
        target = locale_to_deepl.get(lang_code, "EN")

    if target == "EN":
        return {
            "translated_text": consent_text,
            "target_lang": "EN",
            "provider": "DeepL",
            "note": "No translation needed; target is English.",
        }

    return translate_consent_text(
        consent_text,
        target_lang=target,
        auth_key=auth_key,
    )


def translate_idp_consent_pack(
    consent_strings: Dict[str, str],
    target_languages: List[str],
    auth_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a full consent pack (multiple consent strings) into multiple target languages
    using DeepL API.
    """
    all_translations = {}

    for target_lang in target_languages:
        texts = list(consent_strings.values())
        batch_result = translate_consent_batch(
            texts,
            target_lang=target_lang,
            auth_key=auth_key,
        )
        translated_map = {}
        for key, item in zip(consent_strings.keys(), batch_result["translations"]):
            translated_map[key] = item["translated"]
        all_translations[target_lang] = translated_map

    return {
        "translations": all_translations,
        "source_keys": list(consent_strings.keys()),
        "target_languages": target_languages,
        "provider": "DeepL",
    }


if __name__ == "__main__":
    sample_consent = (
        "By clicking Continue, you authorize this application to access your "
        "Google Account profile information and email address."
    )
    result = translate_consent_text(sample_consent, target_lang="DE")
    print("Translated:", result["translated_text"])
