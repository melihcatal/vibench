import os
import requests
from deep_translator import GoogleTranslator

# Provider: Google Cloud Translation API (SDK)
# No extra auth needed for deep_translator lightweight client
translator = GoogleTranslator(source='auto', target='en')

def appeal_translate(appeal_text: str, target_lang: str = 'en') -> str:
    """Translate appeal text into English using Google Cloud Translation.

    Returns the translated string.
    """
    # Using the lightweight wrapper; swap for google-cloud-translate client if needed.
    return translator.translate(appeal_text, dest=target_lang)
