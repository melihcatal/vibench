import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate
from document_models import NormalizedExpense


def translate_invoice_notes(expense: NormalizedExpense, target_language: str = "es") -> Dict[str, Any]:
    client = translate.Client()

    translations = {}
    for item in expense.items:
        if item["description"]:
            result = client.translate(
                item["description"],
                target_language=target_language
            )
            translations[item["description"]] = result["translatedText"]

    return {
        "vendor_merchant": expense.vendor_merchant,
        "translated_items": translations,
        "target_language": target_language
    }