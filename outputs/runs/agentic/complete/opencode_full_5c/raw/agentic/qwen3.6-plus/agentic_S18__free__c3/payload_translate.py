import os
from typing import Optional
from google.cloud import translate_v2 as translate
from messaging_models import EventMessage, normalize_payload


GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "default-project")
TRANSLATE_MODEL = "nmt"


def get_translate_client() -> translate.Client:
    return translate.Client()


def translate_text(
    text: str, target_language: str, source_language: str = None
) -> dict:
    client = get_translate_client()

    kwargs = {
        "q": text,
        "target_language": target_language,
        "format_": "text",
        "model": TRANSLATE_MODEL,
    }
    if source_language:
        kwargs["source_language"] = source_language

    try:
        result = client.translate(**kwargs)
        return {
            "translated_text": result.get("translatedText", ""),
            "detected_source_language": result.get(
                "detectedSourceLanguage", source_language or "unknown"
            ),
            "target_language": target_language,
            "model": TRANSLATE_MODEL,
            "success": True,
        }
    except Exception as exc:
        return {
            "translated_text": text,
            "detected_source_language": "",
            "target_language": target_language,
            "model": TRANSLATE_MODEL,
            "success": False,
            "error": str(exc),
        }


def translate_event_payload(
    event_data: dict, target_language: str, source_language: str = None
) -> dict:
    event = EventMessage.from_dict(event_data)
    payload = normalize_payload(event.payload)

    translated_payload = {}
    translations = []

    for key, value in payload.items():
        if isinstance(value, str) and len(value.strip()) > 0:
            result = translate_text(value, target_language, source_language)
            translated_payload[key] = result["translated_text"]
            translations.append(
                {
                    "field": key,
                    "original": value,
                    "translated": result["translated_text"],
                    "success": result["success"],
                }
            )
        else:
            translated_payload[key] = value

    return {
        "event_id": event.event_id,
        "original_payload": payload,
        "translated_payload": translated_payload,
        "translations": translations,
        "target_language": target_language,
        "model": TRANSLATE_MODEL,
    }
