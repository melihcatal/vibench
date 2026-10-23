import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> str:
    client = translate.Client()

    # Target language can be a language code, e.g. "es" for Spanish, "fr" for French.
    result = client.translate(text, target_language=target_language)
    
    return result['translatedText']