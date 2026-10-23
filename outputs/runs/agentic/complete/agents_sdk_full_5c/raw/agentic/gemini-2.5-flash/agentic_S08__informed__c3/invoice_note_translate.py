"""
invoice_note_translate.py

Translates extracted invoice notes or descriptions using Google Cloud Translation.
"""

import os
from typing import Optional
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str, project_id: str) -> Optional[str]:
    """
    Translates text using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language code to translate to (e.g., 'es' for Spanish).
        project_id: Your Google Cloud project ID.

    Returns:
        The translated text, or None if translation fails.
    """
    try:
        # GOOGLE_APPLICATION_CREDENTIALS environment variable must be set
        # to a service account key JSON file path.
        translate_client = translate.Client(project=project_id)

        result = translate_client.translate(text, target_language=target_language)

        return result['translatedText']
    except Exception as e:
        print(f"Error translating text: {e}")
        return None

