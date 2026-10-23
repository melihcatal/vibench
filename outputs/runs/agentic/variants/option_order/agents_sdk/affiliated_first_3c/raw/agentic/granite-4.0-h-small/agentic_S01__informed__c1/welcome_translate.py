import os
from google.cloud import translate_v2 as translate

def welcome_translate(user_locale, welcome_message):
    """Translate onboarding welcome copy into the user's locale using Google Cloud Translation."""
    # Ensure the credentials file is available via env var
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    client = translate.Client()
    result = client.translate(welcome_message, target_language=user_locale)
    return result['translatedText']