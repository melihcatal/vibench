from google.cloud import translate_v2 as translate
from typing import Dict


def translate_runbook_notes(text: str, target_language: str = "es") -> Dict[str, str]:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }
