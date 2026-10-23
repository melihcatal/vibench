"""
Translate extracted invoice notes or descriptions using Azure AI Translator.

Translates vendor notes, memo fields, or invoice descriptions from source
language to target language using Azure Cognitive Services Translator API.

Provider: Azure AI Translator (Cognitive Services)
SDK: azure-ai-translation-text
API: https://api.cognitive.microsofttranslator.com/translate
"""

import os
from typing import Optional

import requests


AZURE_TRANSLATOR_ENDPOINT = os.environ.get(
    "AZURE_TRANSLATOR_ENDPOINT",
    "https://api.cognitive.microsofttranslator.com/",
)
AZURE_TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION", "")
AZURE_TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY", "")

TRANSLATE_API_URL = "https://api.cognitive.microsofttranslator.com/translate"


def translate_invoice_note(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    region: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    Translate invoice notes or descriptions using Azure AI Translator.

    Uses the Azure Cognitive Services Translator REST API to translate
    vendor-provided text fields from source language to target language.

    Args:
        text: Invoice note, memo, or description text to translate.
        target_language: Target language code (e.g., 'en', 'es', 'fr', 'de', 'ja').
        source_language: Source language code. Auto-detected if None.
        region: Azure Translator region. Falls back to AZURE_TRANSLATOR_REGION env var.
        api_key: Azure Translator API key. Falls back to AZURE_TRANSLATOR_KEY env var.

    Returns:
        Translated text string.

    Raises:
        ValueError: If Azure Translator credentials are not provided.
        requests.RequestException: If the Azure API call fails.
    """
    key = api_key or AZURE_TRANSLATOR_KEY
    translator_region = region or AZURE_TRANSLATOR_REGION

    if not key:
        raise ValueError(
            "Azure Translator API key is required. "
            "Set AZURE_TRANSLATOR_KEY environment variable."
        )

    params = {
        "api-version": "3.0",
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": translator_region,
        "Content-Type": "application/json",
    }

    body = [{"text": text}]

    response = requests.post(
        TRANSLATE_API_URL,
        params=params,
        headers=headers,
        json=body,
        timeout=30,
    )
    response.raise_for_status()

    result = response.json()
    translated_text = result[0]["translations"][0]["text"]
    return translated_text


def translate_vendor_notes(
    notes: dict[str, str],
    target_language: str = "en",
    source_language: Optional[str] = None,
    region: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict[str, str]:
    """
    Translate multiple vendor note fields in a single request.

    Args:
        notes: Dictionary mapping field names to text values.
        target_language: Target language code.
        source_language: Source language code. Auto-detected if None.
        region: Azure Translator region.
        api_key: Azure Translator API key.

    Returns:
        Dictionary mapping field names to translated text.
    """
    if not notes:
        return {}

    key = api_key or AZURE_TRANSLATOR_KEY
    translator_region = region or AZURE_TRANSLATOR_REGION

    if not key:
        raise ValueError("Azure Translator API key is required.")

    params = {
        "api-version": "3.0",
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": translator_region,
        "Content-Type": "application/json",
    }

    body = [{"text": text} for text in notes.values() if text]

    if not body:
        return {k: v for k, v in notes.items()}

    response = requests.post(
        TRANSLATE_API_URL,
        params=params,
        headers=headers,
        json=body,
        timeout=30,
    )
    response.raise_for_status()

    results = response.json()
    translations = [r["translations"][0]["text"] for r in results]

    translated_notes = {}
    idx = 0
    for field_name, text in notes.items():
        if text:
            translated_notes[field_name] = translations[idx]
            idx += 1
        else:
            translated_notes[field_name] = text

    return translated_notes


def translate_invoice_description(
    description: str,
    target_language: str = "en",
    api_key: Optional[str] = None,
    region: Optional[str] = None,
) -> str:
    """
    Convenience function to translate an invoice description field.

    Args:
        description: Invoice description text to translate.
        target_language: Target language code.
        api_key: Azure Translator API key.
        region: Azure Translator region.

    Returns:
        Translated description text.
    """
    return translate_invoice_note(
        text=description,
        target_language=target_language,
        api_key=api_key,
        region=region,
    )
