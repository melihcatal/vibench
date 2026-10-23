"""
consent_translate.py - Translate identity-provider consent copy
Provider: DeepL (deepl.com) - DeepL Translate API
"""

import os
import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_PAID_API_URL = "https://api.deepl.com/v2/translate"


def translate_consent_text(
    source_text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    api_key: Optional[str] = None,
    use_paid_api: bool = False,
) -> Dict[str, Any]:
    """
    Translate identity-provider consent copy using DeepL Translate API.

    Provider: DeepL (deepl.com)
    API: https://www.deepl.com/docs-api
    """
    effective_api_key = api_key or os.environ.get("DEEPL_API_KEY", "")
    if not effective_api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")

    api_url = DEEPL_PAID_API_URL if use_paid_api else DEEPL_API_URL

    payload = {
        "text": source_text,
        "target_lang": target_lang.upper(),
        "tag_handling": "xml",
        "ignore_tags": "code,script",
        "formality": "more",
    }

    if source_lang:
        payload["source_lang"] = source_lang.upper()

    headers = {
        "Authorization": f"DeepL-Auth-Key {effective_api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(api_url, data=payload, headers=headers)
            response.raise_for_status()
            result = response.json()

        translations = result.get("translations", [])
        if not translations:
            return {
                "success": False,
                "error": "No translations returned from DeepL",
                "provider": "deepl",
            }

        translated_text = translations[0].get("text", "")
        detected_source = translations[0].get("detected_source_language", source_lang)

        return {
            "success": True,
            "source_text": source_text,
            "translated_text": translated_text,
            "source_lang": detected_source or source_lang or "unknown",
            "target_lang": target_lang.upper(),
            "provider": "deepl",
            "api_url": api_url,
            "translated_at": datetime.utcnow().isoformat(),
        }
    except httpx.HTTPStatusError as exc:
        return {
            "success": False,
            "error": f"DeepL API HTTP {exc.response.status_code}: {exc.response.text}",
            "provider": "deepl",
        }
    except httpx.RequestError as exc:
        return {
            "success": False,
            "error": f"DeepL request error: {str(exc)}",
            "provider": "deepl",
        }


def translate_consent_bundle(
    consent_texts: Dict[str, str],
    target_lang: str,
    source_lang: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a bundle of consent strings using DeepL.

    consent_texts: dict of {key: text} for consent fields like:
    - "terms_of_service": "By clicking accept, you agree to..."
    - "privacy_policy": "We process your data according to..."
    - "data_sharing": "Your profile data may be shared with..."

    Provider: DeepL (deepl.com)
    """
    results = {}
    all_success = True
    errors = []

    for key, text in consent_texts.items():
        result = translate_consent_text(
            source_text=text,
            target_lang=target_lang,
            source_lang=source_lang,
            api_key=api_key,
        )

        if result["success"]:
            results[key] = result["translated_text"]
        else:
            all_success = False
            errors.append({"key": key, "error": result.get("error", "Unknown error")})
            results[key] = text  # Fallback to original

    return {
        "success": all_success,
        "translated_consent": results,
        "target_lang": target_lang.upper(),
        "source_lang": source_lang,
        "provider": "deepl",
        "errors": errors if errors else None,
        "translated_at": datetime.utcnow().isoformat(),
    }


def get_supported_languages(api_key: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Fetch supported languages from DeepL API.

    Provider: DeepL
    """
    effective_api_key = api_key or os.environ.get("DEEPL_API_KEY", "")
    if not effective_api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")

    headers = {"Authorization": f"DeepL-Auth-Key {effective_api_key}"}

    try:
        with httpx.Client(timeout=15.0) as client:
            response = client.get(
                "https://api-free.deepl.com/v2/languages",
                params={"type": "target"},
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError:
        return []
