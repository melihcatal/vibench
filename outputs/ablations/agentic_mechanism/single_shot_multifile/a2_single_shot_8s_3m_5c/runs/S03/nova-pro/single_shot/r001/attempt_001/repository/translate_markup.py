import os
from google.cloud import translate_v2 as translate

def translate_markup(markup, target_language):
    client = translate.Client(key=os.getenv('GOOGLE_CLOUD_TRANSLATE_API_KEY'))
    result = client.translate(markup, target_language=target_language, format_='html')
    return result['translatedText']