import os
import json
from google.cloud import translate_v2 as translate

client = translate.Client()

def translate_runbook_notes(text: str, target_language: str = 'en') -> str:
    result = client.translate(text, target_language=target_language)
    return result['translatedText']