from google.cloud import translate_v2 as translate
import os
from typing import List, Dict


def translate_text(text: str, target_language: str = "es") -> Dict[str, str]:
    """
    Translates a given text using Google Cloud Translation.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS_PATH"
    )
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": result["input"],
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
