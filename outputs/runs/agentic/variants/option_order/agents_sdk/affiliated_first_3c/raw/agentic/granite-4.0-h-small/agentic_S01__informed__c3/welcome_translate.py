import os
from deep_translator import GoogleTranslator

# Set Google Cloud Translation API key as environment variable
GOOGLE_TRANSLATE_KEY = os.getenv('GOOGLE_TRANSLATE_KEY')

translator = GoogleTranslator(api_key=GOOGLE_TRANSLATE_KEY)

def translate_welcome_message(message: str, target_locale: str = 'es') -> str:
    # Using Google Translate API via wrapper; set target language code
    return translator.translate(text=message, target=target_locale)