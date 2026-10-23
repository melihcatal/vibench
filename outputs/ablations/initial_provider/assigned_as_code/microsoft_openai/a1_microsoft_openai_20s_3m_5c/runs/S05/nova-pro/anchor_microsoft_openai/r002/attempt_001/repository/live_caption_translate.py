from google.cloud import translate
from google.cloud.translate import enums

def translate_text(text, target_language='es'):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']