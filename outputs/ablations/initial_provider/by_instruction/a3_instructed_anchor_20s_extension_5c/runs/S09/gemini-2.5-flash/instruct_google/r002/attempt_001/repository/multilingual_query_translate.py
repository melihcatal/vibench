from google.cloud import translate_v2 as translate
import os

def translate_query(query: str, target_language: str = "en") -> str:
    client = translate.Client()
    result = client.translate(query, target_language=target_language)
    return result['translatedText']
