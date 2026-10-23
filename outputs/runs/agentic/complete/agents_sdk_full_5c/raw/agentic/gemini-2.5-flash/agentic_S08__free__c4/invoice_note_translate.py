import os
from typing import Optional, List
from google.cloud import translate_v2 as translate

def translate_text(
    text_content: str,
    target_language: str,
    project_id: str, # Not directly used by translate_v2 client, but good for consistent signature
    source_language: Optional[str] = None,
) -> Optional[str]:
    """Translates text content using Google Cloud Translation API (v2)."""
    try:
        client = translate.Client()

        # API request
        if source_language:
            result = client.translate(text_content, target_language=target_language, source_language=source_language)
        else:
            result = client.translate(text_content, target_language=target_language)

        return result["translatedText"]

    except Exception as e:
        print(f"Error translating text with Google Cloud Translation API: {e}")
        return None

def translate_invoice_notes(
    notes_text: str,
    target_language: str,
    project_id: str,
    source_language: Optional[str] = None,
) -> Optional[str]:
    """Translates invoice notes or descriptions to a target language."""
    if not notes_text:
        return None
    return translate_text(notes_text, target_language, project_id, source_language)
