import os
import requests
from google.cloud import translate_v2 as translate

# Configure Google Cloud credentials via environment variable
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
TRANSLATE_CLIENT = translate.Client()

LOCALE_TO_TARGET = {
    'en': 'en',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',
    # Add more mappings as needed
}

def translate_onboarding(welcome_text: str, locale: str = 'en') -> str:
    """Translate onboarding copy into the user's locale using Google Translate API.
    Returns the translated string. If the locale is unsupported, returns original text.
    """
    target = LOCALE_TO_TARGET.get(locale, 'en')
    if not target:
        return welcome_text
    try:
        result = TRANSLATE_CLIENT.translate(welcome_text, target_language=target)
        return result.get('translatedText', welcome_text)
    except Exception as e:
        # Fallback gracefully
        return welcome_text
