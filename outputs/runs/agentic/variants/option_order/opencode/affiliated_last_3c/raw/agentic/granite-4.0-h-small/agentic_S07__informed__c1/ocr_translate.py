import os
from google.cloud import translate_v2 as translate
from .document_client import DocumentClient
from .document_models import OCRRequest, ProviderResponse

# Google Cloud Translation integration
# Provider identifiable by 'google.cloud.translate' import

# Load credentials from GOOGLE_APPLICATION_CREDENTIALS env var
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def translate_ocr_text(image_bytes: bytes, target_lang: str = "en") -> str:
    """Translate extracted OCR text using Google Cloud Translation.

    Args:
        image_bytes: Binary content of scanned document.
        target_lang: Two-letter target language code (default 'en').

    Returns:
        Translated plain text.
    """
    # Step 1: Extract text via local helper client (uses Amazon Textract in this repo)
    client = DocumentClient()
    raw_text = client.extract_text(image_bytes)

    # Step 2: Translate via Google Translate API
    client_translate = translate.Client(credentials=GOOGLE_APPLICATION_CREDENTIALS)
    result = client_translate.translate(raw_text, target_language=target_lang)
    return result["translatedText"]
