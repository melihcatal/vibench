import os, json
from google.cloud import translate_v2 as translate

def welcome_translate(user_locale, welcome_text):
    # Google Cloud Translation credentials are expected via GOOGLE_APPLICATION_CREDENTIALS env var
    client = translate.Client()
    result = client.translate(welcome_text, target_language=user_locale)
    return result['translatedText']
