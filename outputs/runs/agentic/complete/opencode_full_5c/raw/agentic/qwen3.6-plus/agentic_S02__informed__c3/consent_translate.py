import os
import json
import time
from typing import Dict, Any, List, Optional

import deepl

from identity_models import UserProfile


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_DEFAULT_SOURCE_LANG = "EN"
DEEPL_DEFAULT_TARGET_LANG = "ES"


def translate_consent_text(
    text: str,
    target_lang: str = DEEPL_DEFAULT_TARGET_LANG,
    source_lang: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    if not api_key:
        api_key = DEEPL_AUTH_KEY

    if not api_key:
        return {
            "success": False,
            "error": "missing_credentials",
            "message": "DeepL API key is required",
            "provider": "deepl",
        }

    translator = deepl.Translator(api_key)

    kwargs = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    result = translator.translate_text(text, **kwargs)

    return {
        "success": True,
        "original_text": text,
        "translated_text": result.text,
        "source_lang": result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else source_lang or "auto",
        "target_lang": target_lang,
        "provider": "deepl",
        "translated_at": time.time(),
    }


def translate_consent_bundle(
    consent_texts: Dict[str, str],
    target_lang: str = DEEPL_DEFAULT_TARGET_LANG,
    source_lang: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    if not api_key:
        api_key = DEEPL_AUTH_KEY

    if not api_key:
        return {
            "success": False,
            "error": "missing_credentials",
            "message": "DeepL API key is required",
            "provider": "deepl",
        }

    translator = deepl.Translator(api_key)

    translations = {}
    for key, text in consent_texts.items():
        kwargs = {"target_lang": target_lang}
        if source_lang:
            kwargs["source_lang"] = source_lang

        result = translator.translate_text(text, **kwargs)
        translations[key] = {
            "original": text,
            "translated": result.text,
            "detected_source": result.detected_source_lang
            if hasattr(result, "detected_source_lang")
            else source_lang or "auto",
        }

    return {
        "success": True,
        "translations": translations,
        "target_lang": target_lang,
        "provider": "deepl",
        "translated_at": time.time(),
    }


def translate_identity_provider_consent(
    provider_name: str,
    consent_text: str,
    target_languages: Optional[List[str]] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    if not api_key:
        api_key = DEEPL_AUTH_KEY

    if not target_languages:
        target_languages = ["ES", "FR", "DE", "JA", "ZH"]

    if not api_key:
        return {
            "success": False,
            "error": "missing_credentials",
            "message": "DeepL API key is required",
            "provider": "deepl",
        }

    translator = deepl.Translator(api_key)

    translations = {}
    for lang in target_languages:
        result = translator.translate_text(consent_text, target_lang=lang)
        translations[lang] = result.text

    return {
        "success": True,
        "provider_name": provider_name,
        "original_text": consent_text,
        "translations": translations,
        "provider": "deepl",
        "translated_at": time.time(),
    }


def get_supported_languages(api_key: Optional[str] = None) -> Dict[str, Any]:
    if not api_key:
        api_key = DEEPL_AUTH_KEY

    if not api_key:
        return {
            "success": False,
            "error": "missing_credentials",
            "message": "DeepL API key is required",
            "provider": "deepl",
        }

    translator = deepl.Translator(api_key)

    source_languages = translator.get_source_languages()
    target_languages = translator.get_target_languages()

    return {
        "success": True,
        "source_languages": [
            {"code": lang.code, "name": lang.name} for lang in source_languages
        ],
        "target_languages": [
            {"code": lang.code, "name": lang.name} for lang in target_languages
        ],
        "provider": "deepl",
        "retrieved_at": time.time(),
    }


if __name__ == "__main__":
    sample_consent = "By clicking Continue, you authorize this application to access your profile information from the identity provider."
    result = translate_consent_text(sample_consent, target_lang="ES")
    print(json.dumps(result, indent=2))
