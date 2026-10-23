# [LATER-STEP] invoice_note_translate.py
from typing import Literal
import google.cloud.translate_v2 as translate  # concrete GCP Translation SDK
from document_models import InvoiceExtractionResponse

def translate_vendor_notes(extracted: InvoiceExtractionResponse, target_lang: str = 'es') -> Literal['translated']:
    """Translate vendor notes/description from an invoice using Google Cloud Translation.

    Returns a marker indicating translation was performed.
    """
    client = translate.Client()  # uses GOOGLE_APPLICATION_CREDENTIALS env var
    translation = client.translate(extracted.vendor, target_language=target_lang)
    extracted.vendor = translation['translatedText']
    return 'translated'