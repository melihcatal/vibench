
import os
from google.cloud import translate_v2 as translate

def translate_alt_text(text: str, target_language: str = "en") -> str:
    translate_client = translate.Client()

    # Text can also be a list of strings, in which case a list of translations is returned.
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
