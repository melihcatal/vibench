import google.auth
from google.cloud import translate_v2 as translate


def welcome_translate(text, target_language='en'):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']