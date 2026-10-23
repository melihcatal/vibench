import os
from document_client import OcrClient
from document_models import OCRResponse
from google.cloud import translate_v2 as translate


def translate_ocr_text(image_path: str, target_lang: str = "en") -> str:
    """Translate extracted OCR text using Google Cloud Translation.

    Prerequisites: set environment variables GOOGLE_APPLICATION_CREDENTIALS and PROVIDER=google.
    """
    # Step 1: extract text
    client = OcrClient()
    ocr_result = client.process_document(open(image_path, "rb").read())
    raw_text = ocr_result.text  # simplified extraction of text from provider response

    # Step 2: translate text
    translate_client = translate.Client()
    translation = translate_client.translate(raw_text, target_language=target_lang)
    return translation["translatedText"]
