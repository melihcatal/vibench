"""Translate customer-facing message payload text using Google Cloud Translation API.

Translates message payloads between languages for international
Pub/Sub message processing pipelines.
"""

import json
from typing import List, Dict, Any, Optional

from google.cloud import translate_v2 as translate

from messaging_client import get_pubsub_config
from messaging_models import ConsumedMessage, normalize_payload

_GOOGLE_TRANSLATE_MODEL_ID = "nmt"


def translate_message_payload(
    message: ConsumedMessage,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    """Translate a message payload using Google Cloud Translation API.

    Args:
        message: ConsumedMessage with payload to translate.
        target_language: Target language code (e.g., 'en', 'es', 'fr').
        source_language: Source language code, auto-detect if None.

    Returns:
        Dictionary with translated payload and metadata.
    """
    payload = normalize_payload(message.payload)
    text_content = _extract_translatable_text(payload)

    if not text_content:
        return {
            "message_id": message.message_id,
            "event_id": message.event_id,
            "original_language": "unknown",
            "target_language": target_language,
            "translated_payload": payload,
            "translation_status": "no_text_to_translate",
        }

    client = translate.Client()

    translate_args = {
        "values": [text_content],
        "target_language": target_language,
        "format_": "text",
    }

    if source_language:
        translate_args["source_language"] = source_language

    result = client.translate(**translate_args)

    translation = result[0] if isinstance(result, list) else result
    translated_text = translation["translatedText"]
    detected_source = translation.get("detectedSourceLanguage", source_language or "auto")

    translated_payload = _apply_translation_to_payload(
        payload, translated_text
    )

    return {
        "message_id": message.message_id,
        "event_id": message.event_id,
        "original_language": detected_source,
        "target_language": target_language,
        "original_text": text_content,
        "translated_text": translated_text,
        "translated_payload": translated_payload,
        "translation_status": "translated",
        "model": _GOOGLE_TRANSLATE_MODEL_ID,
    }


def batch_translate_messages(
    messages: List[ConsumedMessage],
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Batch translate multiple message payloads using Google Cloud Translation API.

    Args:
        messages: List of ConsumedMessage objects.
        target_language: Target language code.
        source_language: Source language code, auto-detect if None.

    Returns:
        List of translation results.
    """
    results = []
    for msg in messages:
        result = translate_message_payload(
            msg,
            target_language=target_language,
            source_language=source_language,
        )
        results.append(result)
    return results


def translate_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    """Translate arbitrary text using Google Cloud Translation API.

    Args:
        text: Text to translate.
        target_language: Target language code.
        source_language: Source language code.

    Returns:
        Dictionary with translation result.
    """
    client = translate.Client()

    translate_args = {
        "values": [text],
        "target_language": target_language,
        "format_": "text",
    }

    if source_language:
        translate_args["source_language"] = source_language

    result = client.translate(**translate_args)
    translation = result[0] if isinstance(result, list) else result

    return {
        "original_text": text,
        "translated_text": translation["translatedText"],
        "detected_source_language": translation.get(
            "detectedSourceLanguage", source_language or "auto"
        ),
        "target_language": target_language,
        "model": _GOOGLE_TRANSLATE_MODEL_ID,
    }


def _extract_translatable_text(payload: Dict[str, Any]) -> str:
    """Extract text fields from a payload for translation.

    Args:
        payload: Normalized payload dictionary.

    Returns:
        Combined text string for translation.
    """
    translatable_keys = [
        "text", "message", "content", "body", "description",
        "title", "subject", "summary", "comment",
    ]

    text_parts = []
    for key in translatable_keys:
        if key in payload and isinstance(payload[key], str):
            text_parts.append(payload[key])

    if not text_parts:
        for value in payload.values():
            if isinstance(value, str) and len(value) > 3:
                text_parts.append(value)

    return " ".join(text_parts) if text_parts else ""


def _apply_translation_to_payload(
    payload: Dict[str, Any], translated_text: str
) -> Dict[str, Any]:
    """Apply translated text back to the payload structure.

    Args:
        payload: Original payload.
        translated_text: Translated text content.

    Returns:
        Updated payload with translated text.
    """
    translated = dict(payload)
    translated["translated"] = True

    for key in ["text", "message", "content", "body"]:
        if key in translated and isinstance(translated[key], str):
            translated[key] = translated_text
            break
    else:
        translated["translated_text"] = translated_text

    return translated
