"""Translate encryption or compliance notes for reviewers using DeepL API."""

import os
from typing import Optional

import requests

from security_models import TranslateRequest, TranslateResponse


DEEPL_API_BASE = "https://api-free.deepl.com/v2"
DEEPL_PRO_API_BASE = "https://api.deepl.com/v2"


def get_deepl_api_base() -> str:
    """Determine which DeepL API endpoint to use based on auth key."""
    return DEEPL_API_BASE


def translate_compliance_note(
    text: str,
    source_lang: str = "auto",
    target_lang: str = "en",
    auth_key: Optional[str] = None,
) -> TranslateResponse:
    """Translate encryption or compliance notes for reviewers.

    Uses the DeepL Translation API to convert compliance documentation,
    encryption policy notes, or audit findings between languages.

    Supported source/target languages include:
    EN (English), DE (German), FR (French), ES (Spanish), IT (Italian),
    NL (Dutch), PL (Polish), PT (Portuguese), RU (Russian), JA (Japanese),
    ZH (Chinese), KO (Korean), BG (Bulgarian), CS (Czech), DA (Danish),
    EL (Greek), FI (Finnish), HU (Hungarian), LT (Lithuanian), LV (Latvian),
    NB (Norwegian), RO (Romanian), SK (Slovak), SL (Slovenian), SV (Swedish),
    TR (Turkish), UK (Ukrainian).

    Args:
        text: The compliance note text to translate.
        source_lang: Source language code (auto for auto-detection).
        target_lang: Target language code.
        auth_key: DeepL API key. If None, reads DEEPL_AUTH_KEY env var.

    Returns:
        TranslateResponse with translated text and language codes.
    """
    if auth_key is None:
        auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable must be set.")

    api_base = get_deepl_api_base()
    url = f"{api_base}/translate"

    payload = {
        "text": text,
        "target_lang": target_lang.upper(),
    }
    if source_lang and source_lang.lower() != "auto":
        payload["source_lang"] = source_lang.upper()

    headers = {
        "Authorization": f"DeepL-Auth-Key {auth_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()

    result = response.json()
    translations = result.get("translations", [])
    if not translations:
        raise ValueError("No translations returned from DeepL API.")

    translation = translations[0]
    translated_text = translation.get("text", "")
    detected_source = translation.get("detected_source_language", source_lang)

    return TranslateResponse(
        translated_text=translated_text,
        source_lang=detected_source,
        target_lang=target_lang.upper(),
    )


def translate_bulk_compliance_notes(
    notes: list,
    target_lang: str = "en",
    auth_key: Optional[str] = None,
) -> list:
    """Translate multiple compliance notes in a single API call.

    Args:
        notes: List of compliance note texts.
        target_lang: Target language code.
        auth_key: DeepL API key.

    Returns:
        List of TranslateResponse objects.
    """
    if auth_key is None:
        auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable must be set.")

    api_base = get_deepl_api_base()
    url = f"{api_base}/translate"

    payload = {
        "text": notes,
        "target_lang": target_lang.upper(),
    }

    headers = {
        "Authorization": f"DeepL-Auth-Key {auth_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()

    result = response.json()
    translations = result.get("translations", [])

    results = []
    for translation in translations:
        results.append(TranslateResponse(
            translated_text=translation.get("text", ""),
            source_lang=translation.get("detected_source_language", "auto"),
            target_lang=target_lang.upper(),
        ))

    return results


if __name__ == "__main__":
    note = "Datenverschlüsselung gemäß DSGVO-Anforderungen mit AES-256 durchgeführt. Schlüsselrotation alle 90 Tage. Alle verschlüsselten Datensätze sind im Audit-Protokoll verzeichnet."
    result = translate_compliance_note(note, source_lang="DE", target_lang="EN")
    print(f"Source: {result.source_lang}")
    print(f"Target: {result.target_lang}")
    print(f"Translation: {result.translated_text}")
