# [LATER-STEP] invoice_note_translate.py
"""
Translate extracted invoice notes or descriptions using Google Cloud Translation API.
"""
import json
from google.cloud import translate_v2
from document_models import InvoiceExtractionResponse

def translate_notes(extracted: InvoiceExtractionResponse) -> InvoiceExtractionResponse:
    """Translate vendor or description fields to target language.

    Args:
        extracted: Original extraction dict.

    Returns:
        Dict with translated strings.
    """
    client = translate_v2.Client()  # uses GOOGLE_APPLICATION_CREDENTIALS env
    target = "es"  # Spanish
    for k in ("vendor", "line_items"):
        if k in extracted:
            text = extracted[k] if isinstance(extracted[k], str) else ""
            translation = client.translate(text, target_language=target)
            extracted[k] = translation["translatedText"] if k == "vendor" else translation
    return extracted
