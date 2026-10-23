"""Translate identity-provider consent copy using Azure AI Translator.

This module translates OAuth/OIDC consent text for identity providers
using the Azure AI Translator service.

Provider: Azure AI Translator
SDK: requests (REST API)
Auth env vars: AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION
"""

import os
from typing import List, Optional

import requests

from identity_models import TranslatedConsentText


AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
AZURE_TRANSLATOR_API_VERSION = "3.0"


def translate_consent_text(
    source_text: str,
    target_language: str,
    source_language: Optional[str] = None,
    translator_key: Optional[str] = None,
    translator_region: Optional[str] = None,
) -> TranslatedConsentText:
    """Translate identity provider consent copy using Azure AI Translator.

    Args:
        source_text: The consent text to translate.
        target_language: Target language code (e.g., 'es', 'fr', 'de').
        source_language: Source language code (auto-detected if None).
        translator_key: Azure Translator key (falls back to AZURE_TRANSLATOR_KEY).
        translator_region: Azure Translator region (falls back to AZURE_TRANSLATOR_REGION).

    Returns:
        TranslatedConsentText with the translated content.

    Raises:
        ValueError: If credentials are missing.
        requests.RequestException: If the translation request fails.
    """
    key = translator_key or os.environ.get("AZURE_TRANSLATOR_KEY")
    region = translator_region or os.environ.get("AZURE_TRANSLATOR_REGION")

    if not key:
        raise ValueError("AZURE_TRANSLATOR_KEY environment variable is not set")
    if not region:
        raise ValueError("AZURE_TRANSLATOR_REGION environment variable is not set")

    url = (
        f"{AZURE_TRANSLATOR_ENDPOINT}/translate"
        f"?api-version={AZURE_TRANSLATOR_API_VERSION}"
        f"&to={target_language}"
    )

    if source_language:
        url += f"&from={source_language}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    body = [{"text": source_text}]

    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()

    result = response.json()
    translated = result[0]["translations"][0]["text"]
    detected_source = result[0].get("detectedLanguage", {}).get("language", source_language or "auto")

    return TranslatedConsentText(
        source_text=source_text,
        source_language=detected_source,
        target_language=target_language,
        translated_text=translated,
    )


def translate_consent_batch(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
) -> List[TranslatedConsentText]:
    """Translate multiple consent texts in a single Azure AI Translator request.

    Args:
        texts: List of consent texts to translate.
        target_language: Target language code.
        source_language: Source language code (auto-detected if None).

    Returns:
        List of TranslatedConsentText results.
    """
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not key:
        raise ValueError("AZURE_TRANSLATOR_KEY environment variable is not set")
    if not region:
        raise ValueError("AZURE_TRANSLATOR_REGION environment variable is not set")

    url = (
        f"{AZURE_TRANSLATOR_ENDPOINT}/translate"
        f"?api-version={AZURE_TRANSLATOR_API_VERSION}"
        f"&to={target_language}"
    )

    if source_language:
        url += f"&from={source_language}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    body = [{"text": t} for t in texts]

    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()

    results = response.json()
    translations = []

    for i, result in enumerate(results):
        translated = result["translations"][0]["text"]
        detected = result.get("detectedLanguage", {}).get("language", source_language or "auto")
        translations.append(
            TranslatedConsentText(
                source_text=texts[i],
                source_language=detected,
                target_language=target_language,
                translated_text=translated,
            )
        )

    return translations


def translate_consent_with_glossary(
    source_text: str,
    target_language: str,
    glossary_terms: Optional[dict] = None,
) -> TranslatedConsentText:
    """Translate consent text with optional glossary term replacement.

    Args:
        source_text: The consent text to translate.
        target_language: Target language code.
        glossary_terms: Dictionary of term mappings to apply post-translation.

    Returns:
        TranslatedConsentText with translated and glossary-adjusted text.
    """
    result = translate_consent_text(source_text, target_language)

    if glossary_terms:
        translated = result.translated_text
        for source_term, target_term in glossary_terms.items():
            translated = translated.replace(source_term, target_term)
        result.translated_text = translated

    return result


if __name__ == "__main__":
    sample = "By clicking Continue, you agree to share your profile data with this application."
    result = translate_consent_text(sample, "es")
    print(f"Translated: {result.translated_text}")
