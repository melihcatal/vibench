"""
[LATER-STEP] Translate extracted invoice notes or descriptions.
Uses Azure AI Translator (Azure Cognitive Services Translator API) to translate
invoice notes, descriptions, and memo fields from the source language to a
target language (default: English).

Provider: Azure AI Translator
SDK: requests (REST API)
Endpoint: https://api.cognitive.microsofttranslator.com
Model: Azure Neural Machine Translation
"""

import os
import logging
from typing import Optional, Dict, Any, List

import requests
import uuid

from document_models import InvoiceExtractionResult
from document_client import get_azure_translator_config, validate_provider_config

logger = logging.getLogger(__name__)

# Azure Translator API endpoint hostname
AZURE_TRANSLATOR_HOST = "api.cognitive.microsofttranslator.com"
AZURE_TRANSLATOR_BASE_URL = "https://api.cognitive.microsofttranslator.com"


def translate_invoice_notes(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate invoice notes or descriptions using Azure AI Translator.

    Args:
        text: Text content to translate.
        target_language: Target language code (ISO 639-1, default: "en").
        source_language: Source language code (auto-detected if None).

    Returns:
        Dictionary with original text, translated text, and detected language.
    """
    config = get_azure_translator_config()
    if not validate_provider_config("azure_translator", config):
        raise ValueError("Azure Translator configuration is incomplete. "
                        "Set AZURE_TRANSLATOR_KEY environment variable.")

    subscription_key = config["subscription_key"]
    region = config["region"]
    endpoint = config["endpoint"]

    # Azure Translator API requires UUID for request identification
    request_id = str(uuid.uuid4())

    # Build request URL for translation
    translate_url = f"{endpoint}/translate"
    params = {
        "api-version": "3.0",
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    # Build request headers with Azure subscription key
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
        "X-ClientTraceId": request_id,
    }

    # Build request body
    body = [{"text": text}]

    try:
        logger.info(
            f"Translating text with Azure Translator: {AZURE_TRANSLATOR_HOST} "
            f"(source: {source_language or 'auto'}, target: {target_language})"
        )

        # Call Azure Translator REST API
        response = requests.post(
            translate_url,
            params=params,
            headers=headers,
            json=body,
            timeout=30,
        )
        response.raise_for_status()

        # Parse translation response
        result = response.json()
        translation = result[0]["translations"][0]["text"]
        detected_language = result[0].get("detectedLanguage", {}).get("language", "unknown")

        return {
            "original_text": text,
            "translated_text": translation,
            "source_language": source_language or detected_language,
            "target_language": target_language,
            "confidence": result[0].get("detectedLanguage", {}).get("score", 0.0),
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Azure Translator API error: {str(e)}")
        raise


def translate_invoice_line_items(
    invoice: InvoiceExtractionResult,
    target_language: str = "en",
) -> InvoiceExtractionResult:
    """
    Translate all invoice line item descriptions using Azure AI Translator.

    Args:
        invoice: InvoiceExtractionResult with line items to translate.
        target_language: Target language code.

    Returns:
        InvoiceExtractionResult with translated line item descriptions.
    """
    # Collect all description texts for batch translation
    texts_to_translate = []
    for item in invoice.line_items:
        if item.description:
            texts_to_translate.append({"description": item.description})

    if not texts_to_translate:
        return invoice

    # Translate each description (Azure Translator supports batch in single request)
    batch_body = [{"text": item["description"]} for item in texts_to_translate]

    config = get_azure_translator_config()
    subscription_key = config["subscription_key"]
    region = config["region"]
    endpoint = config["endpoint"]

    translate_url = f"{endpoint}/translate"
    params = {"api-version": "3.0", "to": target_language}
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    try:
        response = requests.post(
            translate_url,
            params=params,
            headers=headers,
            json=batch_body,
            timeout=30,
        )
        response.raise_for_status()
        results = response.json()

        # Update line items with translated descriptions
        for i, item in enumerate(invoice.line_items):
            if i < len(results):
                translation = results[i]["translations"][0]["text"]
                item.description = translation

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to batch translate line items: {str(e)}")

    return invoice


def translate_vendor_memo(memo: str, target_language: str = "en") -> Dict[str, Any]:
    """
    Translate a vendor memo or note using Azure AI Translator.

    Args:
        memo: Vendor memo text to translate.
        target_language: Target language code.

    Returns:
        Translation result dictionary.
    """
    return translate_invoice_notes(memo, target_language=target_language)


def detect_language(text: str) -> Dict[str, Any]:
    """
    Detect the language of invoice text using Azure Translator.

    Args:
        text: Text to analyze.

    Returns:
        Dictionary with detected language and confidence.
    """
    config = get_azure_translator_config()
    subscription_key = config["subscription_key"]
    region = config["region"]
    endpoint = config["endpoint"]

    detect_url = f"{endpoint}/detect"
    params = {"api-version": "3.0"}
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }
    body = [{"text": text}]

    response = requests.post(detect_url, params=params, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    result = response.json()[0]

    return {
        "language": result.get("language", "unknown"),
        "confidence": result.get("score", 0.0),
        "is_translation_supported": result.get("isTranslationSupported", False),
    }
