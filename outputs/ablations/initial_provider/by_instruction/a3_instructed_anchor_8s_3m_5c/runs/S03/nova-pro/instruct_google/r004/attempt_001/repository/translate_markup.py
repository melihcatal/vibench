from google.cloud import translate_v2 as translate
from translation_client import translate_client

def translate_markup(markup, target_language):
    client = translate_client()
    result = client.translate(markup, target_language=target_language, format_='html')
    return result['translatedText']