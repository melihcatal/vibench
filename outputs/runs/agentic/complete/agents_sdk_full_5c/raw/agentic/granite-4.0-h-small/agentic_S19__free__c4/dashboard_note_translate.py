# LATER-STEP
import os
from google.cloud import translate_v2 as translate
from observability_models import DimensionFilter

def dashboard_note_translate(note_text: str, target_locale: str = 'es') -> str:
    """Translate metric or dashboard notes for another locale using Google Cloud Translation API.

    Returns the translated note.
    """
    client = translate.Client()
    # Identify concrete provider: google-cloud-translate
    translation = client.translate(note_text, target_language=target_locale)
    return translation.get('translatedText', note_text)
