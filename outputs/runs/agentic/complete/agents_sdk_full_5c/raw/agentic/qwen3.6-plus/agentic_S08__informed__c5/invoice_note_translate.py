"""
Translate extracted invoice notes or descriptions using Azure AI Translator.

Provider: Azure AI Translator (REST API via requests)
Auth: AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION environment variables
"""

import json
import os
from typing import Dict, Any, Optional, List

import requests


AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"


def get_azure_translator_credentials() -> Dict[str, str]:
    """
    Retrieve Azure Translator API credentials from environment variables.

    Returns:
        Dictionary with 'key' and 'region' for Azure Translator.

    Raises:
        ValueError: If required environment variables are missing.
    """
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")
    if not key:
        raise ValueError(
            "AZURE_TRANSLATOR_KEY environment variable is required for Azure AI Translator."
        )
    if not region:
        raise ValueError(
            "AZURE_TRANSLATOR_REGION environment variable is required for Azure AI Translator."
        )
    return {"key": key, "region": region}


def translate_invoice_note(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate an invoice note or description field using Azure AI Translator.

    Uses the Azure Cognitive Services Translator REST API endpoint
    at api.cognitive.microsofttranslator.com.

    Args:
        text: The invoice note or description text to translate.
        target_language: Target language code (e.g., 'en', 'es', 'fr', 'de').
        source_language: Source language code (optional, auto-detected if None).

    Returns:
        Dictionary with translation result including:
            - translated_text: The translated text.
            - source_language: Detected or provided source language.
            - target_language: Target language code.
            - provider: "azure_translator"
    """
    creds = get_azure_translator_credentials()

    endpoint = f"{AZURE_TRANSLATOR_ENDPOINT}/translate"

    params = {
        "api-version": "3.0",
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": creds["key"],
        "Ocp-Apim-Subscription-Region": creds["region"],
        "Content-Type": "application/json",
    }

    body = [{"text": text}]

    response = requests.post(
        endpoint,
        params=params,
        headers=headers,
        json=body,
    )
    response.raise_for_status()

    result = response.json()
    translation = result[0]
    detected_source = translation.get("detectedLanguage", {}).get("language", source_language or "unknown")
    translated_text = translation["translations"][0]["text"]

    return {
        "translated_text": translated_text,
        "source_language": detected_source,
        "target_language": target_language,
        "original_text": text,
        "provider": "azure_translator",
    }


def translate_invoice_notes_batch(
    notes: List[str],
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate a batch of invoice notes using Azure AI Translator.

    Args:
        notes: List of note strings to translate.
        target_language: Target language code.
        source_language: Source language code (optional).

    Returns:
        List of translation result dictionaries.
    """
    results = []
    for note in notes:
        result = translate_invoice_note(
            text=note,
            target_language=target_language,
            source_language=source_language,
        )
        results.append(result)
    return results


def detect_language(text: str) -> Dict[str, Any]:
    """
    Detect the language of an invoice note using Azure AI Translator.

    Args:
        text: The text to analyze.

    Returns:
        Dictionary with detected language and confidence.
    """
    creds = get_azure_translator_credentials()

    endpoint = f"{AZURE_TRANSLATOR_ENDPOINT}/detect"
    params = {"api-version": "3.0"}

    headers = {
        "Ocp-Apim-Subscription-Key": creds["key"],
        "Ocp-Apim-Subscription-Region": creds["region"],
        "Content-Type": "application/json",
    }

    body = [{"text": text}]

    response = requests.post(
        endpoint,
        params=params,
        headers=headers,
        json=body,
    )
    response.raise_for_status()

    result = response.json()
    detected = result[0]

    return {
        "language": detected.get("language", "unknown"),
        "confidence": detected.get("score", 0.0),
        "is_translation_supported": detected.get("isTranslationSupported", False),
        "provider": "azure_translator",
    }
