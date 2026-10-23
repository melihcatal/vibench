"""
Translate customer-facing message payload text using Google Cloud Translation API.

Uses the google-cloud-translate SDK (translate_v3) to translate message
payload text between languages. Authenticated via
GOOGLE_APPLICATION_CREDENTIALS.
"""

import os
from typing import Any
from google.cloud import translate_v2 as translate


GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")


def translate_text(
    text: str,
    target_language: str,
    source_language: str | None = None,
    format_type: str = "text",
) -> dict[str, Any]:
    """
    Translate a single text string using Google Cloud Translation API v2.

    Args:
        text: The text content to translate.
        target_language: Target language code (e.g., 'es', 'fr', 'ja').
        source_language: Source language code. If None, auto-detection is used.
        format_type: 'text' or 'html'.

    Returns:
        Dictionary containing the translated text, detected source language,
        and target language.
    """
    client = translate.Client()

    kwargs: dict[str, Any] = {
        "target_language": target_language,
        "format_": format_type,
    }
    if source_language:
        kwargs["source_language"] = source_language

    result = client.translate(text, **kwargs)

    return {
        "translated_text": result.get("translatedText", ""),
        "detected_source_language": result.get("detectedSourceLanguage", source_language or "unknown"),
        "target_language": target_language,
        "original_text": text,
    }


def translate_payload_fields(
    payload: dict[str, Any],
    target_language: str,
    text_fields: list[str] | None = None,
    source_language: str | None = None,
) -> dict[str, Any]:
    """
    Translate specific text fields within a message payload dictionary.

    Args:
        payload: The message payload dictionary.
        target_language: Target language code.
        text_fields: List of field names to translate. If None, all string fields are translated.
        source_language: Source language code. If None, auto-detection is used.

    Returns:
        Dictionary with original payload, translated payload, and per-field translation details.
    """
    if text_fields is None:
        text_fields = [k for k, v in payload.items() if isinstance(v, str)]

    translated_payload = dict(payload)
    translation_details: dict[str, Any] = {}

    for field_name in text_fields:
        if field_name in payload and isinstance(payload[field_name], str):
            result = translate_text(
                text=payload[field_name],
                target_language=target_language,
                source_language=source_language,
            )
            translated_payload[field_name] = result["translated_text"]
            translation_details[field_name] = {
                "original": payload[field_name],
                "translated": result["translated_text"],
                "detected_source": result["detected_source_language"],
            }

    return {
        "original_payload": payload,
        "translated_payload": translated_payload,
        "target_language": target_language,
        "fields_translated": list(translation_details.keys()),
        "translation_details": translation_details,
    }


if __name__ == "__main__":
    import json
    sample_payload = {
        "message": "Welcome to our platform!",
        "description": "Your account has been created successfully.",
        "user_id": "usr_12345",
    }
    result = translate_payload_fields(
        payload=sample_payload,
        target_language="es",
    )
    print(json.dumps(result, indent=2))
