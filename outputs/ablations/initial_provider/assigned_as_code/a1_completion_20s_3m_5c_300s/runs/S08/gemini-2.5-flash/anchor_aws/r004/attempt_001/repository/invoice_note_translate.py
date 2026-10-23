import os
from typing import Dict, Any, List
from google.cloud import translate_v2 as translate

def translate_invoice_notes(notes: List[str], target_language: str = "en") -> Dict[str, Any]:
    # Set up Google Cloud Translation client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or configure authentication
    translate_client = translate.Client()

    translated_notes: List[str] = []
    for note in notes:
        try:
            result = translate_client.translate(note, target_language=target_language)
            translated_notes.append(result["translatedText"])
        except Exception as e:
            translated_notes.append(f"Translation failed for '{note}': {e}")
    
    return {"original_notes": notes, "translated_notes": translated_notes, "target_language": target_language}
