from google.cloud import translate_v3 as translate
import os
from typing import Optional
from document_client import get_document_client, load_config
from document_models import TranslationResponse


def translate_ocr_text(text: str, target_language: str = "es") -> TranslationResponse:
    """
    Translates extracted OCR text using Google Cloud Translation.

    Args:
        text: The text extracted from OCR to translate.
        target_language: Target language code (e.g., "es", "fr", "de").

    Returns:
        TranslationResponse containing the translated text and metadata.
    """
    client = get_document_client("google_translate")
    config = load_config("google_translate")

    project_id = config.get("project_id")
    location = config.get("location", "global")

    if not project_id:
        raise ValueError(
            "Google Cloud project ID must be set in environment variables."
        )

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    source_language = response.translations[0].detected_language_code

    return TranslationResponse(
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
        provider="google_cloud_translation",
        model="v3",
    )
