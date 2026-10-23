import os
import requests
from typing import Optional, Dict, Any, List
from identity_models import (
    ConsentTranslationRequest,
    ConsentTranslationResult,
)


DEEPL_API_URL = "https://api.deepl.com/v2"
DEEPL_FREE_API_URL = "https://api-free.deepl.com/v2"


def translate_consent_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
    context: Optional[str] = None,
    formal: bool = True,
) -> ConsentTranslationResult:
    if api_key is None:
        api_key = os.environ.get("DEEPL_API_KEY", "")

    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")

    is_free_tier = api_key.endswith(":fx")
    base_url = DEEPL_FREE_API_URL if is_free_tier else DEEPL_API_URL

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    body = {
        "text": text,
        "target_lang": target_language.upper(),
        "preserve_formatting": "1",
    }

    if source_language:
        body["source_lang"] = source_language.upper()

    if context:
        body["context"] = context

    if formal:
        body["formality"] = "more"
    else:
        body["formality"] = "less"

    response = requests.post(
        f"{base_url}/translate",
        headers=headers,
        data=body,
        timeout=30,
    )
    response.raise_for_status()
    result_data = response.json()

    translations = result_data.get("translations", [])
    if not translations:
        raise ValueError("No translations returned from DeepL API")

    translation = translations[0]
    translated_text = translation.get("text", "")
    detected_source = translation.get("detected_source_language", source_language)

    return ConsentTranslationResult(
        translated_text=translated_text,
        source_language=detected_source or source_language or "unknown",
        target_language=target_language,
        detected_language=detected_source,
        confidence=1.0,
        raw_response=result_data,
    )


def translate_consent_copy(
    request: ConsentTranslationRequest,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    if api_key is None:
        api_key = os.environ.get("DEEPL_API_KEY", "")

    result = translate_consent_text(
        text=request.text,
        target_language=request.target_language,
        source_language=request.source_language,
        api_key=api_key,
        context=request.context,
    )

    return {
        "success": True,
        "translation": {
            "original_text": request.text,
            "translated_text": result.translated_text,
            "source_language": result.source_language,
            "target_language": result.target_language,
            "detected_language": result.detected_language,
            "confidence": result.confidence,
        },
    }


def batch_translate_consent(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
    context: Optional[str] = None,
) -> List[ConsentTranslationResult]:
    if api_key is None:
        api_key = os.environ.get("DEEPL_API_KEY", "")

    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")

    is_free_tier = api_key.endswith(":fx")
    base_url = DEEPL_FREE_API_URL if is_free_tier else DEEPL_API_URL

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    body = {
        "target_lang": target_language.upper(),
    }

    if source_language:
        body["source_lang"] = source_language.upper()

    if context:
        body["context"] = context

    for i, text in enumerate(texts):
        body[f"text[{i}]"] = text

    response = requests.post(
        f"{base_url}/translate",
        headers=headers,
        data=body,
        timeout=30,
    )
    response.raise_for_status()
    result_data = response.json()

    results = []
    translations = result_data.get("translations", [])
    for i, translation in enumerate(translations):
        results.append(
            ConsentTranslationResult(
                translated_text=translation.get("text", ""),
                source_language=translation.get(
                    "detected_source_language", source_language or "unknown"
                ),
                target_language=target_language,
                detected_language=translation.get("detected_source_language"),
                confidence=1.0,
                raw_response=result_data,
            )
        )

    return results


def get_supported_consent_languages(
    api_key: Optional[str] = None,
) -> List[Dict[str, str]]:
    if api_key is None:
        api_key = os.environ.get("DEEPL_API_KEY", "")

    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")

    is_free_tier = api_key.endswith(":fx")
    base_url = DEEPL_FREE_API_URL if is_free_tier else DEEPL_API_URL

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
    }

    response = requests.get(
        f"{base_url}/languages",
        headers=headers,
        params={"type": "target"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def translate_auth0_consent_terms(
    consent_text: str,
    target_languages: List[str],
    api_key: Optional[str] = None,
) -> Dict[str, str]:
    if api_key is None:
        api_key = os.environ.get("DEEPL_API_KEY", "")

    translations = {}
    for lang in target_languages:
        result = translate_consent_text(
            text=consent_text,
            target_language=lang,
            api_key=api_key,
            context="identity provider consent terms",
        )
        translations[lang] = result.translated_text

    return translations
