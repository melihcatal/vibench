"""
ocr_translate.py - Translate extracted OCR text using Azure AI Translator.

Provider: Azure AI Translator (part of Azure Cognitive Services)
Endpoint: api.cognitive.microsofttranslator.com
"""

from typing import Optional, Dict, Any, List

import requests
from azure.core.credentials import AzureKeyCredential

from document_client import (
    DocumentClientConfig,
    prepare_text_payload,
)
from document_models import OcrTextResult


def translate_ocr_text(
    ocr_result: OcrTextResult,
    target_language: str = "en",
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate extracted OCR text using Azure AI Translator REST API.

    Args:
        ocr_result: OcrTextResult from OCR extraction.
        target_language: Target language code (e.g., "en", "es", "fr").
        source_language: Source language code (None for auto-detect).
        api_key: Azure Translator subscription key.
        endpoint: Azure Translator endpoint URL.
        region: Azure Translator region (e.g., "eastus").

    Returns:
        Dictionary with translated text and metadata.
    """
    api_key = api_key or DocumentClientConfig.AZURE_TRANSLATOR_KEY
    endpoint = endpoint or DocumentClientConfig.AZURE_TRANSLATOR_ENDPOINT
    region = region or DocumentClientConfig.AZURE_TRANSLATOR_REGION

    text_to_translate = ocr_result.extracted_text
    if not text_to_translate or not text_to_translate.strip():
        return {
            "original_text": "",
            "translated_text": "",
            "target_language": target_language,
            "source_language": "unknown",
        }

    # Build translation URL: Azure Translator v3.0
    translate_url = f"{endpoint}translate?api-version=3.0&to={target_language}"
    if source_language:
        translate_url += f"&from={source_language}"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    body = [{"text": text_to_translate}]

    try:
        response = requests.post(
            translate_url,
            headers=headers,
            json=body,
            timeout=DocumentClientConfig.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Azure Translator API call failed: {e}") from e

    translation_data = response.json()

    translated_text = ""
    detected_language = source_language or "auto"

    if translation_data and len(translation_data) > 0:
        result_item = translation_data[0]
        if "translations" in result_item:
            translations = result_item["translations"]
            if translations:
                translated_text = translations[0].get("text", "")
        if "detectedLanguage" in result_item:
            detected_language = result_item["detectedLanguage"].get("language", detected_language)

    return {
        "original_text": text_to_translate,
        "translated_text": translated_text,
        "target_language": target_language,
        "source_language": detected_language,
        "confidence": ocr_result.confidence,
    }


def translate_lines(
    ocr_result: OcrTextResult,
    target_language: str = "en",
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    region: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate individual OCR lines preserving layout structure.

    Args:
        ocr_result: OcrTextResult from OCR extraction.
        target_language: Target language code.
        source_language: Source language code.
        api_key, endpoint, region: Azure Translator credentials.

    Returns:
        List of translated line objects with original and translated text.
    """
    api_key = api_key or DocumentClientConfig.AZURE_TRANSLATOR_KEY
    endpoint = endpoint or DocumentClientConfig.AZURE_TRANSLATOR_ENDPOINT
    region = region or DocumentClientConfig.AZURE_TRANSLATOR_REGION

    lines = ocr_result.lines if ocr_result.lines else []
    line_texts = [line.get("text", "") for line in lines if line.get("text", "")]

    if not line_texts:
        return []

    translate_url = f"{endpoint}translate?api-version=3.0&to={target_language}"
    if source_language:
        translate_url += f"&from={source_language}"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    body = [{"text": t} for t in line_texts if t.strip()]

    try:
        response = requests.post(
            translate_url,
            headers=headers,
            json=body,
            timeout=DocumentClientConfig.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Azure Translator line-level translation failed: {e}") from e

    translation_data = response.json()
    translated_lines = []

    for idx, line in enumerate(lines):
        original_text = line.get("text", "")
        translated_text = ""
        detected = "auto"

        if idx < len(translation_data):
            item = translation_data[idx]
            if "translations" in item and item["translations"]:
                translated_text = item["translations"][0].get("text", "")
            if "detectedLanguage" in item:
                detected = item["detectedLanguage"].get("language", "auto")

        translated_lines.append({
            "original_text": original_text,
            "translated_text": translated_text,
            "source_language": detected,
            "target_language": target_language,
            "bounding_box": line.get("bounding_box"),
            "words": line.get("words", []),
        })

    return translated_lines
