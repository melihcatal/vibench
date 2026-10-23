from __future__ import annotations

import os

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from document_models import OCRResponse

AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY", "")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "")
AZURE_TRANSLATOR_TARGET_LANGUAGE = os.getenv("AZURE_TRANSLATOR_TARGET_LANGUAGE", "en")


def translate_ocr_text(ocr_response: OCRResponse, target_language: str = AZURE_TRANSLATOR_TARGET_LANGUAGE) -> str:
    if not AZURE_TRANSLATOR_ENDPOINT or not AZURE_TRANSLATOR_KEY or not AZURE_TRANSLATOR_REGION:
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION are required")
    client = TextTranslationClient(endpoint=AZURE_TRANSLATOR_ENDPOINT, credential=AzureKeyCredential(AZURE_TRANSLATOR_KEY), region=AZURE_TRANSLATOR_REGION)
    response = client.translate(content=[ocr_response.text], to=[target_language])
    return response[0].translations[0].text
