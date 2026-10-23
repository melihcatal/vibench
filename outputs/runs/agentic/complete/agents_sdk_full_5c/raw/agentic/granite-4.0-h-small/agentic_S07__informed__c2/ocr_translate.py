import os
import requests
from google.cloud import translate_v2 as translate

# Service identifier:
# Provider: Google Cloud Translation (text translation)

API_KEY = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # set env var to service account JSON path
TRANSLATE_ENDPOINT = 'https://translation.googleapis.com/language/translate/v2'

def translate_text(text: str, target_lang: str = 'en') -> str:
    """Translate extracted OCR text using Google Cloud Translation API.

    Args:
        text: raw OCR string.
        target_lang: target language code (e.g., 'es', 'fr').

    Returns:
        Translated text string.
    """
    # Google client library handles authentication via env var automatically
    client = translate.Client()
    result = client.translate(text, target_language=target_lang)
    return result['translatedText']
