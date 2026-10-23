from google.cloud import translate_v2 as translate
from typing import Dict, Any

client = translate.Client()


def translate_document_fields(
    document: Dict[str, Any], target_language: str = "es"
) -> Dict[str, Any]:
    translated = {}
    for key, value in document.items():
        if isinstance(value, str) and len(value) > 0:
            result = client.translate(value, target_language=target_language)
            translated[key] = result["translatedText"]
        else:
            translated[key] = value
    return translated
