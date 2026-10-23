import os
from google.cloud import translate_v2 as translate

client = translate.Client(os.getenv('GOOGLE_CLOUD_API_KEY'))

def translate_text(text, target_language='en'):
    translation = client.translate(text, target_language=target_language)
    return translation['translatedText']