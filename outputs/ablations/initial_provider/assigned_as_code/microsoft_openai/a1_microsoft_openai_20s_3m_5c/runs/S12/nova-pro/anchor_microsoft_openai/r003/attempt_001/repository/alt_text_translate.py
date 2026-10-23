import google.auth
from google.cloud import translate_v2 as translate

def translate_description(description, target_language='es'):
    translate_client = translate.Client()
    translation = translate_client.translate(description, target_language=target_language)
    return translation['translatedText']