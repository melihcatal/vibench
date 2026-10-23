from google.cloud import translate_v2 as translate
import os

# Initialize Google Cloud Translate client
translate_client = translate.Client()


def translate_compliance_note(text: str, target_language: str = "es") -> dict:
    if not isinstance(text, str) or not text.strip():
        return {
            "translated_text": "",
            "detected_language": "",
            "target_language": target_language,
        }

    result = translate_client.translate(text, target_language=target_language)
    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_language": result["detectedSourceLanguage"],
        "target_language": target_language,
        "provider": "google_translate",
    }


def detect_language(text: str) -> dict:
    if not isinstance(text, str) or not text.strip():
        return {"language": "", "confidence": 0.0}

    result = translate_client.detect_language(text)
    return {
        "language": result["language"],
        "confidence": result["confidence"],
        "provider": "google_translate",
    }
