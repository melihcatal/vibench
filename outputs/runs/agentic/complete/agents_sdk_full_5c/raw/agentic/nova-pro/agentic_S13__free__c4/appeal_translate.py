import os
from google.cloud import translate_v2 as translate

client = translate.Client(api_key=os.getenv('GOOGLE_CLOUD_TRANSLATE_API_KEY'))

def translate_appeal(text, target_language='es'):
    translation = client.translate(text, target_language=target_language)
    return translation['translatedText']