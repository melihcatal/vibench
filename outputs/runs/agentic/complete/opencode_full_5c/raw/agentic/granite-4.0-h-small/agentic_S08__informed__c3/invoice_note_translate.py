# invoice_note_translate.py
# Translate extracted invoice notes or descriptions using Google Cloud Translation
import os
from google.cloud import translate_v2 as translate
from document_models import ExpenseResponse

TRANSLATOR = translate.Client()
TARGET_LANG = 'es'  # example: translate to Spanish

def translate_notes(expense: ExpenseResponse) -> ExpenseResponse:
    """Translate any free‑form note fields in the expense record.",
    # Simple approach: translate the top‑level 'notes' field and each line item description
    if 'notes' in expense:
        translation = TRANSLATOR.translate(expense['notes'], target_language=TARGET_LANG)
        expense['notes'] = translation['translatedText']
    if 'line_items' in expense:
        for item in expense['line_items']:
            if 'description' in item:
                translation = TRANSLATOR.translate(item['description'], target_language=TARGET_LANG)
                item['description'] = translation['translatedText']
    return expense
