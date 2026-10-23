import os
from typing import Any, Dict

# Later-step: translate metric or dashboard notes for another locale using Google Cloud Translation SDK

# Google Cloud credentials (application default)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError('Missing GOOGLE_APPLICATION_CREDENTIALS environment variable')

from google.cloud import translate_v2 as translate

def translate_note(note_text: str, target_locale: str = 'es') -> str:
    """Translate a metric or dashboard note to the target locale.",
    """Uses Google Cloud Translation API.",
    """
    client = translate.Client()
    result = client.translate(note_text, target_language=target_locale)
    return result['translatedText']
