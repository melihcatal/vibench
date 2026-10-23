"""
Translate generated image descriptions using Azure AI Translator.

Provider: Azure AI Translator
SDK: azure-ai-translation-text / REST
Auth: AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION
"""

import os
import json
from typing import List, Optional, Dict, Any

import requests

from describe_image import ImageDescriptionResponse
from image_summary import summarize_visual_analysis


# Azure Translator endpoint (global)
_AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"


def translate_alt_text(
    text: str,
    target_language: str = "es",
    source_language: Optional[str] = None,
    translator_key: Optional[str] = None,
    translator_region: Optional[str] = None,
) -> str:
    """
    Translate a single image description / alt text using Azure AI Translator.

    Args:
        text: The text to translate.
        target_language: Target language code (e.g., 'es', 'fr', 'ja', 'zh-Hans').
        source_language: Source language code (auto-detect if None).
        translator_key: Azure Translator key override.
        translator_region: Azure Translator region override.

    Returns:
        Translated text string.
    """
    key = translator_key or os.environ.get("AZURE_TRANSLATOR_KEY")
    region = translator_region or os.environ.get("AZURE_TRANSLATOR_REGION", "global")

    if not key:
        raise ValueError("AZURE_TRANSLATOR_KEY environment variable must be set")

    endpoint = f"{_AZURE_TRANSLATOR_ENDPOINT}/translate"

    params = {
        "api-version": "3.0",
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    body = [{"text": text}]

    response = requests.post(endpoint, params=params, headers=headers, json=body)
    response.raise_for_status()

    result = response.json()
    if result and result[0].get("translations"):
        return result[0]["translations"][0]["text"]

    return text


def translate_image_description(
    description_response: ImageDescriptionResponse,
    target_languages: Optional[List[str]] = None,
    translator_key: Optional[str] = None,
    translator_region: Optional[str] = None,
) -> Dict[str, Dict[str, str]]:
    """
    Translate all image descriptions into multiple target languages.

    Args:
        description_response: Output from describe_image.
        target_languages: List of target language codes (default: ['es', 'fr', 'de', 'ja']).
        translator_key: Azure Translator key override.
        translator_region: Azure Translator region override.

    Returns:
        Dict mapping language code to translated descriptions.
    """
    if target_languages is None:
        target_languages = ["es", "fr", "de", "ja"]

    translations: Dict[str, Dict[str, str]] = {}

    for lang in target_languages:
        lang_translations = {}
        for i, desc in enumerate(description_response.descriptions):
            translated = translate_alt_text(
                text=desc.text,
                target_language=lang,
                translator_key=translator_key,
                translator_region=translator_region,
            )
            lang_translations[f"description_{i}"] = translated
        translations[lang] = lang_translations

    return translations


def translate_generated_alt_text(
    image_description_response: ImageDescriptionResponse,
    summary_text: Optional[str] = None,
    target_languages: Optional[List[str]] = None,
    translator_key: Optional[str] = None,
    translator_region: Optional[str] = None,
) -> Dict[str, Dict[str, str]]:
    """
    Translate both raw image descriptions and a Gemini-generated summary.

    Uses Azure AI Translator to translate alt text and visual summaries
    into multiple target languages for internationalized accessibility.

    Args:
        image_description_response: Output from describe_image.
        summary_text: Optional summary string from image_summary.
        target_languages: List of target language codes.
        translator_key: Azure Translator key override.
        translator_region: Azure Translator region override.

    Returns:
        Dict with translated descriptions and summary per language.
    """
    results = translate_image_description(
        description_response=image_description_response,
        target_languages=target_languages,
        translator_key=translator_key,
        translator_region=translator_region,
    )

    if summary_text:
        for lang in (target_languages or ["es", "fr", "de", "ja"]):
            translated_summary = translate_alt_text(
                text=summary_text,
                target_language=lang,
                translator_key=translator_key,
                translator_region=translator_region,
            )
            results[lang]["summary"] = translated_summary

    return results


def format_translated_alt_text(
    translations: Dict[str, Dict[str, str]],
) -> str:
    """Format translated alt text into a human-readable report."""
    lines = ["Translated image descriptions:"]
    for lang, lang_data in translations.items():
        lines.append(f"\n  Language: {lang}")
        for key, value in lang_data.items():
            lines.append(f"    [{key}] {value}")
    return "\n".join(lines)
