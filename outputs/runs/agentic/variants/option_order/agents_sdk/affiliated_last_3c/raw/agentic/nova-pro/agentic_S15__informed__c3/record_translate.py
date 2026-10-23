import os
from google.cloud import translate_v2 as translate

translate_client = translate.Client(credentials=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

def translate_text(text, target_language='es'):
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']