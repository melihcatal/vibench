import os
from google.cloud import translate_v2 as translate

# Concrete provider: Google Cloud Translation
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
TRANSLATOR = translate.Client()


def translate_onboarding(copy_en: str, target_locale: str) -> str:
    """Translate onboarding copy from English to the user's locale.

    Args:
        copy_en: original English text
        target_locale: ISO language code (e.g., 'fr', 'es')
    Returns:
        translated text.
    """
    result = TRANSLATOR.translate(copy_en, target_language=target_locale)
    return result['translatedText']
