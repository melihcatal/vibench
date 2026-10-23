import os
import json
from typing import Dict, Any, List, Optional
from google.cloud import translate_v2 as translate


def translate_message_payload(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    message_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Translate customer-facing message payload text using Google Cloud Translation API."""
    client = translate.Client()

    try:
        if source_language:
            result = client.translate(
                text,
                target_language=target_language,
                source_language=source_language,
                format_="text",
            )
        else:
            result = client.translate(
                text, target_language=target_language, format_="text"
            )

        detected_language = result.get("detectedSourceLanguage", source_language)

        return {
            "message_id": message_id,
            "original_text": text,
            "translated_text": result["translatedText"],
            "source_language": detected_language,
            "target_language": target_language,
            "confidence": 1.0,
            "provider": "google-cloud-translation",
        }
    except Exception as e:
        return {
            "message_id": message_id,
            "original_text": text,
            "error": str(e),
            "provider": "google-cloud-translation",
        }


def translate_json_payload(
    payload: Dict[str, Any],
    target_language: str = "en",
    fields_to_translate: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Translate specific fields in a JSON payload."""
    if fields_to_translate is None:
        fields_to_translate = ["title", "description", "content", "message", "body"]

    translated_payload = payload.copy()
    translation_results = {}

    for field in fields_to_translate:
        if field in payload and isinstance(payload[field], str):
            result = translate_message_payload(
                payload[field], target_language=target_language
            )

            if "translated_text" in result:
                translated_payload[field] = result["translated_text"]
                translation_results[field] = {
                    "original": payload[field],
                    "translated": result["translated_text"],
                    "source_language": result.get("source_language"),
                    "target_language": target_language,
                }
            else:
                translation_results[field] = {
                    "error": result.get("error", "Translation failed")
                }

    return {
        "translated_payload": translated_payload,
        "translation_results": translation_results,
        "target_language": target_language,
        "provider": "google-cloud-translation",
    }


def batch_translate_messages(
    messages: List[Dict[str, Any]], target_language: str = "en"
) -> Dict[str, Any]:
    """Batch translate multiple messages."""
    client = translate.Client()
    results = []

    texts_to_translate = []
    message_info = []

    for i, message in enumerate(messages):
        text = message.get("text", "")
        if isinstance(message, dict) and "text" not in message:
            text = json.dumps(message)

        texts_to_translate.append(text)
        message_info.append(
            {
                "index": i,
                "message_id": message.get("message_id", message.get("id", f"msg_{i}")),
                "original": message,
            }
        )

    try:
        batch_results = client.translate(
            texts_to_translate, target_language=target_language, format_="text"
        )

        for i, (info, result) in enumerate(zip(message_info, batch_results)):
            results.append(
                {
                    "message_id": info["message_id"],
                    "original_text": texts_to_translate[i],
                    "translated_text": result["translatedText"],
                    "source_language": result.get("detectedSourceLanguage", "unknown"),
                    "target_language": target_language,
                    "confidence": 1.0,
                    "provider": "google-cloud-translation",
                }
            )
    except Exception as e:
        return {
            "error": str(e),
            "total_messages": len(messages),
            "translated": 0,
            "provider": "google-cloud-translation",
        }

    return {
        "total_messages": len(messages),
        "translated": len(results),
        "target_language": target_language,
        "results": results,
        "provider": "google-cloud-translation",
    }


def detect_language(text: str) -> Dict[str, Any]:
    """Detect the language of text using Google Cloud Translation API."""
    client = translate.Client()

    try:
        result = client.detect_language(text)

        return {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "detected_language": result["language"],
            "confidence": result["confidence"],
            "provider": "google-cloud-translation",
        }
    except Exception as e:
        return {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "error": str(e),
            "provider": "google-cloud-translation",
        }


def get_supported_languages(target_language: str = "en") -> Dict[str, Any]:
    """Get list of supported languages from Google Cloud Translation API."""
    client = translate.Client()

    try:
        languages = client.get_languages(target_language=target_language)

        return {
            "languages": [
                {"code": lang["language"], "name": lang["name"]} for lang in languages
            ],
            "total_languages": len(languages),
            "target_language": target_language,
            "provider": "google-cloud-translation",
        }
    except Exception as e:
        return {"error": str(e), "provider": "google-cloud-translation"}


def create_translation_config(
    default_target: str = "en",
    auto_detect: bool = True,
    cache_translations: bool = True,
) -> Dict[str, Any]:
    """Create translation configuration."""
    return {
        "default_target_language": default_target,
        "auto_detect_source": auto_detect,
        "cache_translations": cache_translations,
        "fields_to_translate": ["title", "description", "content", "message", "body"],
        "batch_size": 100,
        "provider": "google-cloud-translation",
    }


if __name__ == "__main__":
    test_text = "Hola, este es un mensaje de prueba para traducción."
    translation_result = translate_message_payload(test_text, target_language="en")
    print(f"Translation result: {json.dumps(translation_result, indent=2)}")

    lang_detection = detect_language(test_text)
    print(f"Language detection: {json.dumps(lang_detection, indent=2)}")
