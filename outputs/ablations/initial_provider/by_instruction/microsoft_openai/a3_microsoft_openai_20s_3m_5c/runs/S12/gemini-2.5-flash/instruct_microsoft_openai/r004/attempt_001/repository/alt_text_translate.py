import os
from google.cloud import translate_v2 as translate
from vision_models import TranslatedTextResult

def translate_alt_text(text: str, target_language: str = "en") -> TranslatedTextResult:
    client = translate.Client()

    result = client.translate(text, target_language=target_language)
    translated_text = result["translatedText"]

    return TranslatedTextResult(translated_text=translated_text)
