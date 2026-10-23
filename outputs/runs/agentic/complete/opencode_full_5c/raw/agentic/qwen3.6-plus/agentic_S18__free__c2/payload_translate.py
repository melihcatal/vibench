import os
import json
from typing import Any

from google.cloud import translate_v2 as translate

from messaging_models import PubSubEvent


GOOGLE_CLOUD_PROJECT_ENV = "GCP_PROJECT_ID"
DEFAULT_TARGET_LANGUAGE = "en"


def _get_translate_client() -> translate.Client:
    return translate.Client()


def translate_payload_text(
    text: str,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: str | None = None,
) -> dict[str, Any]:
    client = _get_translate_client()

    params = {"q": text, "target": target_language}
    if source_language:
        params["source"] = source_language

    result = client.translate(**params)

    return {
        "original_text": text,
        "translated_text": result.get("translatedText", ""),
        "detected_source_language": result.get(
            "detectedSourceLanguage", source_language or "unknown"
        ),
        "target_language": target_language,
        "model_used": "google-cloud-translate-v2",
    }


def translate_event_payload(
    event: PubSubEvent,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: str | None = None,
) -> dict[str, Any]:
    payload_text = json.dumps(event.payload, default=str)

    translation_result = translate_payload_text(
        text=payload_text,
        target_language=target_language,
        source_language=source_language,
    )

    translated_payload = (
        json.loads(translation_result["translated_text"])
        if translation_result["translated_text"]
        else {}
    )

    return {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "original_payload": event.payload,
        "translated_payload": translated_payload,
        "translation_details": translation_result,
    }


def translate_customer_message(
    message_text: str,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    format_output: bool = True,
) -> dict[str, Any]:
    translation = translate_payload_text(
        text=message_text,
        target_language=target_language,
    )

    if format_output:
        return {
            "customer_message": translation["translated_text"],
            "language": target_language,
            "provider": "google-cloud-translate-v2",
        }

    return translation


if __name__ == "__main__":
    sample_text = "Hola, necesito ayuda con mi pedido numero 12345."
    result = translate_payload_text(sample_text, target_language="en")
    print(json.dumps(result, indent=2))
