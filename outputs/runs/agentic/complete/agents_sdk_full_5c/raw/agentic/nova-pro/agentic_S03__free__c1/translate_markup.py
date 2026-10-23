from google.cloud import translate_v2 as translate
import re

def translate_markup(markup, target_language):
    client = translate.Client()
    text = re.sub(r'<.*?>', '', markup)
    result = client.translate(text, target_language=target_language)
    translated_text = result['translatedText']
    translated_markup = re.sub(text, translated_text, markup)
    return translated_markup