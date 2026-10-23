import os
from typing import List

from document_models import TextExtractionResult

GOOGLE_CLOUD_TRANSLATION_API_KEY = os.getenv("GOOGLE_CLOUD_TRANSLATION_API_KEY", "")


def translate_ocr_text(text_result: TextExtractionResult, target_language: str = "es") -> str:
    from google.cloud import translate_v2 as translate

    if not GOOGLE_CLOUD_TRANSLATION_API_KEY:
        raise RuntimeError("Google Cloud Translation API key is required")
    client = translate.Client()
    response = client.translate(text_result.text, target_language=target_language)
    return str(response.get("translatedText", ""))
