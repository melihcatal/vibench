# [LATER-STEP] welcome_translate.py - Translate onboarding copy into the user's locale
# Provider: Google Cloud Translation

import os
from google.cloud import translate_v2 as translate

def welcome_translate(text: str, target_language: str) -> str:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']
