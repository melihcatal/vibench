import os
from typing import Dict, Any
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate

load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Initialize Google Translate client (uses env credentials by default)
client = translate.Client()


def translate_consent_text(text: str, target_lang: str = 'es') -> str:
    """
    Translate identity‑provider consent copy into another language using Google Cloud Translation.
    Returns the translated string.
    """
    result = client.translate(text, target_language=target_lang)
    return result['translatedText']

# Demo (not executed in production)
if __name__ == '__main__':
    copy_example = (
        "We may collect your name, email, and profile picture for authentication."
    )
    print('Translated consent:', translate_consent_text(copy_example, 'fr'))

# End of consent_translate.py