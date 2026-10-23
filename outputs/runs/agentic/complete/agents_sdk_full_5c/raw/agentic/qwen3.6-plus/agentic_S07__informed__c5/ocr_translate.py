"""
ocr_translate.py - Translate extracted OCR text using Azure AI Translator.

Provider: Azure AI Translator
SDK: azure-ai-translation-text (requests-based REST)
Auth: AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION
"""

import os
import uuid
import requests


AZURE_TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY", "")
AZURE_TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION", "")
AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"


def translate_text(text: str, target_language: str = "en", source_language: str | None = None) -> dict:
    """
    Translate extracted OCR text using Azure AI Translator.

    Args:
        text: The text to translate.
        target_language: Target language code (e.g., 'en', 'fr', 'es').
        source_language: Source language code (e.g., 'fr', 'es'). If None, auto-detected.

    Returns:
        dict with 'translated_text' and 'detected_language' keys.
    """
    if not AZURE_TRANSLATOR_KEY or not AZURE_TRANSLATOR_REGION:
        raise ValueError(
            "Set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables."
        )

    path = "/translate"
    constructed_url = AZURE_TRANSLATOR_ENDPOINT + path

    params = {
        "api-version": "3.0",
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": text}]

    response = requests.post(
        constructed_url,
        params=params,
        headers=headers,
        json=body,
    )
    response.raise_for_status()
    result = response.json()

    translation = result[0]
    translated_text = translation["translations"][0]["text"]
    detected_language = translation.get("detectedLanguage", {})
    detected_lang_code = detected_language.get("language", "unknown") if detected_language else "unknown"

    return {
        "translated_text": translated_text,
        "detected_language": detected_lang_code,
    }


def translate_ocr_blocks(
    blocks: list[str],
    target_language: str = "en",
    source_language: str | None = None,
) -> list[str]:
    """
    Translate a list of OCR text blocks using Azure AI Translator.

    Args:
        blocks: List of text strings to translate.
        target_language: Target language code.
        source_language: Source language code (optional for auto-detect).

    Returns:
        List of translated text strings.
    """
    if not AZURE_TRANSLATOR_KEY or not AZURE_TRANSLATOR_REGION:
        raise ValueError(
            "Set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables."
        )

    path = "/translate"
    constructed_url = AZURE_TRANSLATOR_ENDPOINT + path

    params = {
        "api-version": "3.0",
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": block} for block in blocks]

    response = requests.post(
        constructed_url,
        params=params,
        headers=headers,
        json=body,
    )
    response.raise_for_status()
    results = response.json()

    translated_blocks = []
    for item in results:
        if item.get("translations"):
            translated_blocks.append(item["translations"][0]["text"])
        else:
            translated_blocks.append("")

    return translated_blocks
