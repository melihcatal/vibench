import os
from google.cloud import translate_v2 as translate
from document_models import Invoice


def invoice_note_translate(invoice: Invoice, target_language: str = "es") -> str:
    # This example assumes a 'notes' field could exist on an Invoice.
    # We will simulate this by translating the vendor name as an example.
    note_to_translate = invoice.vendor_name

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    translate_client = translate.Client()

    if isinstance(note_to_translate, bytes):
        note_to_translate = note_to_translate.decode("utf-8")

    result = translate_client.translate(
        note_to_translate, target_language=target_language
    )

    return result["translatedText"]
