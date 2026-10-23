import os
from google.cloud import translate_v2 as translate
from typing import List, Dict

def translate_runbook_notes(
    notes: List[str],
    target_language: str,
    source_language: str = "en"
) -> Dict[str, str]:
    """
    Translates secret-rotation runbook notes using Google Cloud Translate API.

    Args:
        notes: A list of runbook notes (strings) to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'es', 'fr').
        source_language: The ISO 639-1 code for the source language.

    Returns:
        A dictionary mapping original notes to their translated versions.
    """
    # The GOOGLE_APPLICATION_CREDENTIALS env var must be set for this to work
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        # The library will try to find credentials elsewhere, but this is the most common method.

    translate_client = translate.Client()

    if isinstance(notes, str):
        notes = [notes]

    translated_notes = {}
    
    try:
        # The v2 API can handle a list of strings directly
        results = translate_client.translate(
            notes,
            target_language=target_language,
            source_language=source_language
        )
        
        for i, result in enumerate(results):
            original_text = notes[i]
            translated_text = result["translatedText"]
            translated_notes[original_text] = translated_text
            
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return {note: f"Translation Error: {e}" for note in notes}

    return translated_notes
