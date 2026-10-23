import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any, List
from document_models import NormalizedExpense

def translate_invoice_notes(notes_text: str, target_language: str, expense: NormalizedExpense, config=None) -> Dict[str, Any]:
    config = config or {}
    client = translate.Client()

    # The target language for translation
    # For example, "es" for Spanish, "fr" for French

    translation_result = client.translate(notes_text, target_language=target_language)
    
    translated_notes = {
        "original_text": notes_text,
        "translated_text": translation_result["translatedText"],
        "detected_source_language": translation_result["detectedSourceLanguage"],
        "target_language": target_language
    }
    expense.translated_notes = translated_notes
    return translated_notes
