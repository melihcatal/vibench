import os
import json
from typing import Dict, Optional
from google.cloud import translate_v2 as translate
from messaging_models import EventMessage


def translate_payload_text(message_data: Dict, target_language: str = "en") -> Dict:
    """Translate customer-facing message payload text using Google Cloud Translation API."""
    client = translate.Client()

    event_message = EventMessage.from_dict(message_data)

    if not isinstance(event_message.payload, dict):
        return message_data

    translated_payload = event_message.payload.copy()

    text_fields_to_translate = []
    field_mapping = {}

    for key, value in event_message.payload.items():
        if isinstance(value, str) and len(value.strip()) > 0:
            if any(
                field in key.lower()
                for field in [
                    "message",
                    "text",
                    "content",
                    "description",
                    "feedback",
                    "comment",
                ]
            ):
                text_fields_to_translate.append(value)
                field_mapping[len(text_fields_to_translate) - 1] = key

    if not text_fields_to_translate:
        return message_data

    try:
        translations = client.translate(
            text_fields_to_translate,
            target_language=target_language,
            source_language=None,
        )

        for idx, translation in enumerate(translations):
            field_key = field_mapping[idx]
            translated_payload[field_key] = translation["translatedText"]

        translated_message = {
            "event_type": event_message.event_type,
            "customer_id": event_message.customer_id,
            "timestamp": event_message.timestamp,
            "payload": translated_payload,
            "translation_metadata": {
                "target_language": target_language,
                "original_language": translations[0].get(
                    "detectedSourceLanguage", "unknown"
                ),
                "translated_fields": list(field_mapping.values()),
            },
        }

        print(
            f"Translated {len(text_fields_to_translate)} text fields to {target_language}"
        )
        return translated_message

    except Exception as e:
        print(f"Translation failed: {e}")
        return message_data


def detect_payload_language(message_data: Dict) -> Optional[str]:
    """Detect the language of text in message payload."""
    client = translate.Client()

    event_message = EventMessage.from_dict(message_data)

    if not isinstance(event_message.payload, dict):
        return None

    sample_text = ""
    for value in event_message.payload.values():
        if isinstance(value, str) and len(value.strip()) > 10:
            sample_text = value
            break

    if not sample_text:
        return None

    try:
        result = client.detect_language(sample_text)
        return result["language"]
    except Exception as e:
        print(f"Language detection failed: {e}")
        return None


def translate_batch(messages: List[Dict], target_language: str = "en") -> List[Dict]:
    """Translate a batch of messages."""
    translated_messages = []

    for message in messages:
        translated = translate_payload_text(message, target_language)
        translated_messages.append(translated)

    print(f"Translated {len(translated_messages)} messages to {target_language}")
    return translated_messages


if __name__ == "__main__":
    sample_message = {
        "event_type": "customer_feedback",
        "customer_id": 12345,
        "timestamp": "2024-01-15T10:30:00Z",
        "payload": {
            "feedback": "Excelente servicio! El equipo de soporte fue muy útil.",
            "rating": 5,
            "category": "support",
        },
    }

    translated = translate_payload_text(sample_message, "en")
    print(f"Translated message: {json.dumps(translated, indent=2)}")

    detected_lang = detect_payload_language(sample_message)
    print(f"Detected language: {detected_lang}")
