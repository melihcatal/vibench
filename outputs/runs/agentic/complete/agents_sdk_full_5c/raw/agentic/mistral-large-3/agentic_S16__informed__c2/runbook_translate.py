from google.cloud import translate_v2 as translate
import os

from security_models import TranslationResponse

def runbook_translate(text: str, target_language: str) -> TranslationResponse:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    
    return TranslationResponse(
        translated_text=result['translatedText'],
        source_language=result['detectedSourceLanguage'],
        target_language=target_language
    )