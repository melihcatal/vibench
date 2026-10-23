import os
from google.cloud import translate_v2 as translate

def translate_welcome(user_locale: str, message: str) -> str:
    """Translate onboarding copy into the user's locale using Google Cloud Translation.
    Returns translated text.
    """
    client = translate.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS env var
    result = client.translate(message, target_language=user_locale)
    return result['translatedText']

# Example (not executed):
# welcome_es = translate_welcome('es', 'Welcome to our service!')
# print(welcome_es)
