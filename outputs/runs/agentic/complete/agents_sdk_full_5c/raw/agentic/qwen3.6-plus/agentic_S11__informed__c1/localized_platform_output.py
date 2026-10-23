"""Translate platform model output for another locale using Azure AI Translator.

Uses Azure AI Translator with AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class TranslationResult:
    """Result of Azure AI Translator text translation."""

    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float = 1.0
    raw_response: Optional[list[dict]] = None


_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
_TRANSLATOR_API_VERSION = "3.0"
_TRANSLATOR_KEY_ENV = "AZURE_TRANSLATOR_KEY"
_TRANSLATOR_REGION_ENV = "AZURE_TRANSLATOR_REGION"


def _get_translator_key() -> str:
    key = os.environ.get(_TRANSLATOR_KEY_ENV, "")
    if not key:
        raise ValueError(f"{_TRANSLATOR_KEY_ENV} environment variable is not set")
    return key


def _get_translator_region() -> str:
    region = os.environ.get(_TRANSLATOR_REGION_ENV, "")
    if not region:
        raise ValueError(f"{_TRANSLATOR_REGION_ENV} environment variable is not set")
    return region


def _detect_language(
    text: str,
    key: str,
    region: str,
) -> str:
    """Detect the source language of the text using Azure AI Translator."""
    url = f"{_TRANSLATOR_ENDPOINT}/detect?api-version={_TRANSLATOR_API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    payload = [{"text": text}]

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    if result and len(result) > 0:
        return result[0].get("language", "en")
    return "en"


def localized_platform_output(
    text: str,
    target_language: str = "es",
    source_language: Optional[str] = None,
) -> TranslationResult:
    """Translate platform model output to a target locale using Azure AI Translator.

    Args:
        text: The text to translate.
        target_language: Target language code (e.g., 'es' for Spanish, 'fr' for French,
                         'de' for German, 'ja' for Japanese, 'zh-Hans' for Chinese).
        source_language: Optional source language code. If not provided, language
                         is auto-detected via Azure AI Translator Detect endpoint.

    Returns:
        TranslationResult with translated text and metadata.
    """
    key = _get_translator_key()
    region = _get_translator_region()

    if source_language is None:
        source_language = _detect_language(text, key, region)

    url = f"{_TRANSLATOR_ENDPOINT}/translate?api-version={_TRANSLATOR_API_VERSION}&to={target_language}&from={source_language}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    payload = [{"text": text}]

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    translated_text = ""
    confidence = 1.0

    if result and len(result) > 0:
        translations = result[0].get("translations", [])
        if translations:
            translated_text = translations[0].get("text", "")
        det = result[0].get("detectedLanguage", {})
        confidence = det.get("score", 1.0)
        source_language = det.get("language", source_language)

    return TranslationResult(
        source_text=text,
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
        confidence=confidence,
        raw_response=result,
    )


def translate_batch_platform_outputs(
    texts: list[str],
    target_language: str = "es",
) -> list[TranslationResult]:
    """Translate multiple platform outputs in a single Azure AI Translator request."""
    key = _get_translator_key()
    region = _get_translator_region()

    url = f"{_TRANSLATOR_ENDPOINT}/translate?api-version={_TRANSLATOR_API_VERSION}&to={target_language}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    payload = [{"text": t} for t in texts]

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    results: list[TranslationResult] = []
    for i, item in enumerate(result):
        translated = ""
        conf = 1.0
        source_lang = "en"
        translations = item.get("translations", [])
        if translations:
            translated = translations[0].get("text", "")
        det = item.get("detectedLanguage", {})
        conf = det.get("score", 1.0)
        source_lang = det.get("language", "en")
        results.append(
            TranslationResult(
                source_text=texts[i],
                translated_text=translated,
                source_language=source_lang,
                target_language=target_language,
                confidence=conf,
                raw_response=item,
            )
        )

    return results


if __name__ == "__main__":
    result = localized_platform_output(
        text="The Azure OpenAI service provides enterprise-grade AI capabilities.",
        target_language="es",
    )
    print(f"Original: {result.source_text}")
    print(f"Translated: {result.translated_text}")
    print(f"Source: {result.source_language} -> Target: {result.target_language}")
