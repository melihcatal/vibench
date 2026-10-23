# [LATER-STEP] invoice_note_translate.py
# Translates extracted invoice notes or descriptions using DeepL API

import os
import deepl
from document_models import InvoiceResponse

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
TARGET_LANG = os.getenv(
    "INVOICE_TRANSLATION_LANG", "EN"
)  # default target language (source is auto-detected)

t = deepl.Translator(DEEPL_AUTH_KEY)

TRANSLATION_THRESHOLD = 0.8  # confidence-like threshold; DeepL does not give explicit confidence, using length sanity check instead


def translate_text(text: str) -> str:
    """Translate text to the target language and return result.","""
    try:
        result = t.translate_text(text, target_lang=TARGET_LANG)
        # DeepL may return empty translation for very short strings; fallback to original
        return result.text if len(result.text) > 5 else text
    except Exception as e:
        print("Translation error:", e)
        return text


def translate_invoice_note(invoice: InvoiceResponse) -> InvoiceResponse:
    """
    Translate any free-form note fields (vendor memo, description) on the invoice.","""
    if hasattr(invoice, "memo") and invoice.memo:
        invoice.memo = translate_text(invoice.memo)
    # If provider-specific description fields exist, translate them similarly
    return invoice


if __name__ == "__main__":
    # Demo
    sample_note = "Net payment due within 30 days."
    invoice = InvoiceResponse(
        vendor="Acme Corp", date="2024-09-01", total=456.78, line_items=[]
    )
    invoice.memo = sample_note
    translated = translate_invoice_note(invoice)
    print("Translated memo:", translated.memo if hasattr(translated, "memo") else "N/A")
