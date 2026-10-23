import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any, Optional


def translate_consent_text(text: str, target_language: str = "es") -> str:
    google_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not google_credentials:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    client = translate.Client()

    try:
        result = client.translate(text, target_language=target_language, format_="text")

        return result["translatedText"]

    except Exception as e:
        raise Exception(f"Google Cloud Translation error: {e}")


def translate_consent_terms(
    terms: Dict[str, str], target_language: str = "es"
) -> Dict[str, str]:
    google_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not google_credentials:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    client = translate.Client()

    translated_terms = {}

    for key, text in terms.items():
        try:
            result = client.translate(
                text, target_language=target_language, format_="text"
            )
            translated_terms[key] = result["translatedText"]
        except Exception as e:
            print(f"Error translating {key}: {e}")
            translated_terms[key] = text

    return translated_terms
