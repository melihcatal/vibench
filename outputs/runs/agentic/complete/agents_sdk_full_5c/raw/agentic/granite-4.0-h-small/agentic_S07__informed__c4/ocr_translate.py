import os
from google.cloud import translate_v2 as translate

goog_translator = translate.Client()

def translate_ocr_text(text, target_lang='en'):
    result = goog_translator.translate(text, target_language=target_lang)
    return result['translatedText']
