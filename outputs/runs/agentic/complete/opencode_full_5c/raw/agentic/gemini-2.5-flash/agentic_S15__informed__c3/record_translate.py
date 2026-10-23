import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any


def translate_record_text(
    text_content: str, target_language: str = "es"
) -> Dict[str, Any]:
    translate_client = translate.Client()  # Google Cloud Translation
    result = translate_client.translate(text_content, target_language=target_language)
    return {
        "original_text": text_content,
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }
