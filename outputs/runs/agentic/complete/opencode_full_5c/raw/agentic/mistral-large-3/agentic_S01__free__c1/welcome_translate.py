from typing import Dict
from google.cloud import translate_v2 as translate


def welcome_translate(text: str, target_language: str) -> Dict[str, str]:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
