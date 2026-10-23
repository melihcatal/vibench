import os
from google.cloud import translate_v2 as translate

# Configuration
google_application_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Welcome Translate
def welcome_translate(text, target_language):
    translate_client = translate.Client()
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']