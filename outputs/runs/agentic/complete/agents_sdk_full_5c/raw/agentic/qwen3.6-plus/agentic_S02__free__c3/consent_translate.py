"""
consent_translate.py - Translate identity-provider consent copy using
the DeepL Translation API.
"""

from __future__ import annotations

import json
import logging
import os

import requests

logger = logging.getLogger(__name__)

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", "")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_consent_text(
    text: str,
    target_lang: str,
    source_lang: str | None = None,
    api_key: str = DEEPL_API_KEY,
) -> str:
    """
    Translate identity-provider consent copy using the DeepL API.
    DeepL provides high-quality translations for authorization consent screens.
    """
    if not text.strip():
        return text

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = {
        "text": text,
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        payload["source_lang"] = source_lang.upper()

    response = requests.post(DEEPL_API_URL, headers=headers, data=payload, timeout=15)
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations", [])
    if not translations:
        logger.warning("DeepL returned no translations for consent text")
        return text
    translated = translations[0].get("text", text)
    logger.info(
        "Deepl translation: %s -> %s", text[:60], translated[:60]
    )
    return translated


def translate_consent_copy_set(
    copy_items: list[dict[str, str]],
    target_lang: str,
    source_lang: str | None = None,
    api_key: str = DEEPL_API_KEY,
) -> list[dict[str, str]]:
    """
    Translate a set of consent copy items (e.g., title, description,
    accept_button, deny_button) via DeepL.
    """
    if not api_key:
        logger.warning("DEEPL_API_KEY not set; returning untranslated copy")
        return copy_items

    texts = [item.get("text", "") for item in copy_items]
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = {
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        payload["source_lang"] = source_lang.upper()

    for t in texts:
        payload.setdefault("text", []).append(t)

    # Build proper form data with multiple text params
    from urllib.parse import urlencode as url_enc
    form_data = url_enc(
        [
            ("target_lang", target_lang.upper()),
            *[("text", t) for t in texts],
            *(("source_lang", source_lang.upper()) if source_lang else []),
        ]
    )

    response = requests.post(
        DEEPL_API_URL, headers=headers, data=form_data, timeout=15
    )
    response.raise_for_status()
    data = response.json()

    translations = data.get("translations", [])
    result = []
    for idx, item in enumerate(copy_items):
        translated_text = translations[idx].get("text", item["text"]) if idx < len(translations) else item["text"]
        result.append({
            **item,
            "text": translated_text,
            "source_lang": translations[idx].get("detected_source_language", "") if idx < len(translations) else "",
        })
    return result


def translate_idp_consent_screen(
    screen: dict[str, str],
    target_lang: str,
    source_lang: str | None = None,
    api_key: str = DEEPL_API_KEY,
) -> dict[str, str]:
    """
    Translate all text fields in an IdP consent screen configuration
    (title, description, accept_label, decline_label, etc.) via DeepL.
    """
    items = [
        {"field": key, "text": value} for key, value in screen.items()
        if isinstance(value, str) and value.strip()
    ]
    translated_items = translate_consent_copy_set(
        items, target_lang=target_lang, source_lang=source_lang, api_key=api_key
    )
    result = dict(screen)
    for item in translated_items:
        result[item["field"]] = item["text"]
    return result


if __name__ == "__main__":
    sample_screen = {
        "title": "Authorize Access",
        "description": "This application will access your profile information.",
        "accept_label": "Allow",
        "decline_label": "Deny",
    }
    print(json.dumps(sample_screen, indent=2))
