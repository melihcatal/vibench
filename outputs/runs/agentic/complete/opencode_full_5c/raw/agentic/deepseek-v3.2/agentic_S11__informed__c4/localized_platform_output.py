import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any, List, Optional


def translate_text(
    text: str, target_language: str = "es", source_language: Optional[str] = None
) -> Dict[str, Any]:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    client = translate.Client()

    if source_language:
        result = client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = client.translate(text, target_language=target_language)

    translation_result = {
        "original_text": text,
        "translated_text": result["translatedText"],
        "target_language": target_language,
        "detected_source_language": result.get("detectedSourceLanguage"),
        "provider": "Google Cloud Translation",
    }

    if source_language:
        translation_result["source_language"] = source_language

    return translation_result


def batch_translate(
    texts: List[str], target_language: str = "es", source_language: Optional[str] = None
) -> List[Dict[str, Any]]:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    client = translate.Client()

    if source_language:
        results = client.translate(
            texts, target_language=target_language, source_language=source_language
        )
    else:
        results = client.translate(texts, target_language=target_language)

    translations = []
    for i, result in enumerate(results):
        translation = {
            "original_text": texts[i],
            "translated_text": result["translatedText"],
            "target_language": target_language,
            "detected_source_language": result.get("detectedSourceLanguage"),
            "provider": "Google Cloud Translation",
        }
        if source_language:
            translation["source_language"] = source_language
        translations.append(translation)

    return translations


def detect_language(text: str) -> Dict[str, Any]:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    client = translate.Client()
    result = client.detect_language(text)

    return {
        "text": text,
        "language": result["language"],
        "confidence": result.get("confidence", 0.0),
        "provider": "Google Cloud Translation",
    }


def get_supported_languages() -> List[Dict[str, Any]]:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    client = translate.Client()
    languages = client.get_languages()

    return [{"code": lang["language"], "name": lang["name"]} for lang in languages]
