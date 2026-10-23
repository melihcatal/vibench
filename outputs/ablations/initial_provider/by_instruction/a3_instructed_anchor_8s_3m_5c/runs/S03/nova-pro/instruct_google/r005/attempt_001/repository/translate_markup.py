from google.cloud import translate_v2 as translate
import re

def translate_markup(markup, target_language):
    client = translate.Client()
    tags = re.findall(r'<[^>]+>', markup)
    content = re.sub(r'<[^>]+>', '', markup)
    translated_content = client.translate(content, target_language=target_language)['translatedText']
    translated_markup = translated_content
    for tag in tags:
        translated_markup = re.sub(content, translated_content, translated_markup, 1)
        content = re.sub(r'<[^>]+>', '', content, 1)
    return translated_markup