import os
from google.cloud import translate_v2 as translate
import re

def translate_markup(markup, target_language):
    client = translate.Client()
    translated_texts = []
    for text in re.findall(r'>(.*?)<', markup):
        translated_texts.append(client.translate(text, target_language=target_language)['translatedText'])
    translated_markup = markup
    for original, translated in zip(re.findall(r'>(.*?)<', markup), translated_texts):
        translated_markup = translated_markup.replace(original, translated, 1)
    return translated_markup