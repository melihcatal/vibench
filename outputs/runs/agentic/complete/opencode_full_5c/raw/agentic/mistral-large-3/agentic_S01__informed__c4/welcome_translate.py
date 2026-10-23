from google.cloud import translate_v2 as translate
import os
from typing import Dict


def translate_text(text: str, target_language: str) -> Dict[str, str]:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }


def welcome_translate(welcome_message: str, user_locale: str) -> str:
    translation = translate_text(welcome_message, user_locale)
    return translation["translated_text"]


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 3:
        welcome_message, user_locale = sys.argv[1], sys.argv[2]
        translated = welcome_translate(welcome_message, user_locale)
        print(f"Translated: {translated}")
