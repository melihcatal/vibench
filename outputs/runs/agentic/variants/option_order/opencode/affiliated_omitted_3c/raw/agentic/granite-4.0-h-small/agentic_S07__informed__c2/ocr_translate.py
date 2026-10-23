import os
from google.cloud import translate_v2 as translate

# Translation client loaded from document_client.py for consistency
from document_client import DocumentClient


def translate_text(source_text: str, target_lang: str = "en") -> str:
    """
    Translate extracted OCR text using Google Cloud Translation.

    Args:
        source_text: The raw text extracted from OCR.
        target_lang: Destination language code (default 'en').
    Returns:
        Translated text.
    """
    client = DocumentClient(service="translate")
    # Google's client uses `translate.Client()` pattern; reuse generic client
    translate_client = translate.Client()
    result = translate_client.translate(source_text, target_language=target_lang)
    return result["translatedText"]
