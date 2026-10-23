from typing import Dict, Any
from google.cloud import translate_v2 as translate
from document_models import InvoiceFields


def translate_invoice_notes(invoice_data: InvoiceFields, target_language: str = "es") -> Dict[str, Any]:
    """Translate extracted invoice notes or descriptions using Google Cloud Translation."""
    client = translate.Client()
    translations = {}

    for idx, item in enumerate(invoice_data.line_items):
        result = client.translate(
            item.description,
            target_language=target_language
        )
        translations[f"line_item_{idx}"] = {
            "original": item.description,
            "translated": result['translatedText']
        }

    return translations