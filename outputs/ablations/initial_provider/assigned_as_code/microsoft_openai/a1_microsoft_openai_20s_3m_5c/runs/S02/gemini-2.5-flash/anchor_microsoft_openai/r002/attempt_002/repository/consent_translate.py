import os
from google.cloud import translate_v2 as translate


def translate_consent_copy(text: str, target_language: str) -> dict:
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result['translatedText'],
        "source_language": result['detectedSourceLanguage'],
        "target_language": target_language,
    }
