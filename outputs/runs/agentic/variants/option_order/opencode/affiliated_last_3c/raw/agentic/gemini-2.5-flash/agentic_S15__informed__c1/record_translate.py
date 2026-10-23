from google.cloud import translate_v2 as translate
import os
from typing import List, Dict, Any


def translate_text(texts: List[str], target_language: str) -> List[Dict[str, Any]]:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # with the path to your service account key file.
    translate_client = translate.Client()

    translations = []
    for text in texts:
        result = translate_client.translate(text, target_language=target_language)
        translations.append(
            {
                "original_text": text,
                "translated_text": result["translatedText"],
                "detected_source_language": result["detectedSourceLanguage"],
            }
        )
    return translations
