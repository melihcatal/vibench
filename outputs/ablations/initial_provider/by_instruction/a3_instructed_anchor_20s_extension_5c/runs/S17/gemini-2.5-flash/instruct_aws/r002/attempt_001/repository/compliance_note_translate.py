import os
from google.cloud import translate_v2 as translate
from typing import List

def translate_notes(notes: List[str], target_language: str = 'en') -> List[str]:
    translate_client = translate.Client()
    translations = []
    for note in notes:
        result = translate_client.translate(note, target_language=target_language)
        translations.append(result['translatedText'])
    return translations
