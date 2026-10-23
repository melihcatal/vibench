# [LATER-STEP] dashboard_note_translate.py

import os
from google.cloud import translate_v2 as translate

gc_translate = translate.Client()
# Use environment variable GOOGLE_APPLICATION_CREDENTIALS to load credentials

def translate_note(note: str, target_locale: str = 'es') -> str:
    """Translate a free-text metric or dashboard note to another locale.
    Uses Google Cloud Translation API.
    Args:
        note: The original free-form text.
        target_locale: ISO-639-1 language code (default 'es' for Spanish).
    Returns:
        Translated note string.
    Raises:
        Exception if translation fails.
    """
    try:
        result = gc_translate.translate(note, target_language=target_locale)
        return result['translatedText']
    except Exception as e:
        raise RuntimeError(f"Translation failed: {e}")