"""payload_translate.py - Translate customer-facing message payload text using Google Cloud Translation API."""

import json
import logging
import os
from google.cloud import translate_v2 as translate
from messaging_models import PubSubConsumeResponse

logger = logging.getLogger(__name__)

GOOGLE_TRANSLATE_API_KEY = os.environ.get(
    "GOOGLE_TRANSLATE_API_KEY", "AIza-placeholder-api-key"
)
GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-gcp-project-id")
TRANSLATE_MODEL_NAME = "nmt"

_translate_client = translate.Client()


def translate_message_payload(
    message_response: PubSubConsumeResponse,
    target_language: str = "en",
    source_language: str | None = None,
) -> dict:
    """Translate customer-facing message payload text using Google Cloud Translation API.

    Args:
        message_response: A PubSubConsumeResponse containing the message payload.
        target_language: Target ISO-639-1 language code (e.g., 'en', 'fr', 'es').
        source_language: Optional source language code for detection bypass.

    Returns:
        Dictionary with translated payload and metadata.
    """
    if message_response.payload is None:
        return {
            "message_id": message_response.message_id,
            "translated_payload": None,
            "target_language": target_language,
            "status": "no_content",
        }

    text_fields = _extract_translatable_fields(message_response.payload)

    if not text_fields:
        return {
            "message_id": message_response.message_id,
            "translated_payload": message_response.payload,
            "target_language": target_language,
            "status": "no_text_fields",
        }

    try:
        translated_fields = {}
        for field_name, field_text in text_fields.items():
            kwargs = {
                "q": field_text,
                "target_language": target_language,
                "format_": "text",
                "model_": TRANSLATE_MODEL_NAME,
            }
            if source_language:
                kwargs["source_language"] = source_language

            result = _translate_client.translate(**kwargs)
            translated_fields[field_name] = result["translatedText"]

        translated_payload = {**message_response.payload, **translated_fields}

        logger.info(
            "Translated message_id=%s to %s using Google Translate nmt model",
            message_response.message_id,
            target_language,
        )

        return {
            "message_id": message_response.message_id,
            "translated_payload": translated_payload,
            "target_language": target_language,
            "source_language": result.get("detectedSourceLanguage", source_language),
            "model_used": TRANSLATE_MODEL_NAME,
            "translated_fields": list(translated_fields.keys()),
            "status": "translated",
        }

    except Exception as exc:
        logger.error("Translation failed with Google Cloud Translation API: %s", exc)
        return {
            "message_id": message_response.message_id,
            "translated_payload": None,
            "target_language": target_language,
            "status": "failed",
            "error": str(exc),
        }


def _extract_translatable_fields(payload: dict) -> dict[str, str]:
    """Extract text fields from payload that should be translated."""
    translatable_keys = [
        "text", "message", "body", "content", "description",
        "comment", "title", "subject", "name", "details",
    ]
    text_fields = {}
    for key in translatable_keys:
        if key in payload and isinstance(payload[key], str) and payload[key].strip():
            text_fields[key] = payload[key]
    return text_fields


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_msg = PubSubConsumeResponse(
        message_id="msg_translate_001",
        payload={"text": "Bonjour, votre commande a été expédiée.", "order_id": "ORD-123"},
        attributes={"source_language": "fr"},
        status="consumed",
    )
    result = translate_message_payload(sample_msg, target_language="en")
    print(f"Translation result: {result}")
