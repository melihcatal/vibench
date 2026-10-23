import os
from google.cloud import translate_v2 as translate
from typing import List, Dict

def translate_compliance_notes(notes: List[str], target_language: str) -> Dict[str, str]:
    client = translate.Client()
    translations = client.translate(notes, target_language=target_language)

    return {note: translation['translatedText'] for note, translation in zip(notes, translations)}