import os
from google.cloud import translate_v2 as translate # Provider-specific import
from document_models import NormalizedExpense

# Initialize Google Cloud Translation client
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or running in an environment with appropriate service account permissions.
translate_client = translate.Client()

def translate_invoice_notes(expense: NormalizedExpense, target_language: str = "en") -> str:
    if not expense.notes:
        expense.translated_notes = "N/A - No notes to translate."
        return "N/A - No notes to translate."

    try:
        # Detect source language (optional, but good practice)
        # detection = translate_client.detect_language(expense.notes)
        # source_language = detection["language"]
        
        # Translate the text
        translation = translate_client.translate(
            expense.notes,
            target_language=target_language,
            # source_language=source_language, # If detected
            format_="text"
        )
        
        translated_text = translation["translatedText"]
        expense.translated_notes = translated_text
        return translated_text
    except Exception as e:
        print(f"Error translating invoice notes with Google Cloud Translation API: {e}")
        expense.translated_notes = "Error during translation."
        return "Error during translation."
