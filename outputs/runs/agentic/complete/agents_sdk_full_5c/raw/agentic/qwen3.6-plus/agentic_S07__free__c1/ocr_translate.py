"""
ocr_translate.py - Translates extracted OCR text using Azure Translator.

Provider: Azure Translator (Azure Cognitive Services Translator)
SDK: azure-ai-translation-text
Endpoint: api.cognitive.microsofttranslator.com
"""

import os
from typing import Optional

from document_models import (
    ExtractTextResponse,
    TranslationRequest,
    TranslationResponse,
)

PROVIDER = "azure-translator"
AZURE_TRANSLATOR_ENDPOINT = os.environ.get(
    "AZURE_TRANSLATOR_ENDPOINT",
    "https://api.cognitive.microsofttranslator.com",
)
AZURE_TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION", "")
AZURE_TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY", "")


def translate_text(request: TranslationRequest) -> TranslationResponse:
    """
    Translate extracted OCR text using Azure Translator REST API.

    Args:
        request: TranslationRequest with source text and target language.

    Returns:
        TranslationResponse with translated text and metadata.
    """
    import http.client
    import json
    from urllib.parse import urlencode

    if not request.text:
        raise ValueError("Text is required for translation.")

    if not AZURE_TRANSLATOR_KEY:
        raise EnvironmentError(
            "AZURE_TRANSLATOR_KEY environment variable is required."
        )

    route = "/translate"
    params = {
        "api-version": "3.0",
        "to": request.target_language,
    }
    if request.source_language and request.source_language != "auto":
        params["from"] = request.source_language

    query_string = urlencode(params)
    url = f"{route}?{query_string}"

    body = json.dumps([{"Text": request.text}])

    conn = http.client.HTTPSConnection(
        AZURE_TRANSLATOR_ENDPOINT.replace("https://", "")
    )

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-Type": "application/json",
        "Content-Length": str(len(body)),
    }

    conn.request("POST", url, body=body, headers=headers)
    response = conn.getresponse()
    response_data = response.read().decode("utf-8")
    conn.close()

    result = json.loads(response_data)

    translated = result[0]["translations"][0]["text"]
    detected_language = result[0].get("detectedLanguage", {}).get(
        "language", request.source_language
    )

    return TranslationResponse(
        translated_text=translated,
        detected_source_language=detected_language,
        provider=PROVIDER,
        raw_response={"status": response.status, "body": result},
    )


def translate_ocr_response(
    ocr_response: ExtractTextResponse,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> TranslationResponse:
    """
    Translate the full text from an OCR extraction response.

    Args:
        ocr_response: ExtractTextResponse from OCR extraction.
        target_language: Target language code (e.g., 'en', 'fr', 'es').
        source_language: Source language code or 'auto'.

    Returns:
        TranslationResponse with translated OCR text.
    """
    req = TranslationRequest(
        text=ocr_response.full_text,
        source_language=source_language or "auto",
        target_language=target_language,
    )
    return translate_text(req)


def translate_ocr_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> TranslationResponse:
    """
    Convenience function to translate arbitrary OCR-extracted text.

    Args:
        text: The text to translate.
        target_language: Target language code.
        source_language: Source language code or 'auto'.

    Returns:
        TranslationResponse with translated text.
    """
    req = TranslationRequest(
        text=text,
        source_language=source_language or "auto",
        target_language=target_language,
    )
    return translate_text(req)
