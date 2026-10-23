import os
from google.cloud import translate_v2 as translate
TRANSLATE = translate.Client()

def translate_text(text: str, target_lang: str = "es") -> str:
    return TRANSLATE.translate(text, target_language=target_lang)["translatedText"]