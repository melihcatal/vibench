from __future__ import annotations

import os

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from document_models import OCRResponse, normalize_text


def translate_ocr_text(response: OCRResponse, target_language: str) -> str:
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    key = os.environ.get("AZURE_TRANSLATOR_KEY", "").strip()
    region = os.environ.get("AZURE_TRANSLATOR_REGION", "").strip()
    if not key or not region:
        raise ValueError("AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION are required")
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key), region=region)
    text = normalize_text(response.text)
    result = client.translate(content=[text], to=[target_language])
    return result[0].translations[0].text if result and result[0].translations else ""
