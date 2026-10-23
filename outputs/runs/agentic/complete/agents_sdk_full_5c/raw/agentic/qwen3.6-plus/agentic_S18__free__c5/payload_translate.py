"""Translate customer-facing message payload text using Google Cloud Translation API.

Uses the google.cloud.translate_v3 TranslationServiceClient to translate
message payload text between supported languages for international customers.
"""

import os
from typing import Any

from google.cloud.translate_v3 import TranslationServiceClient


DEFAULT_SOURCE_LANG = os.getenv("TRANSLATE_SOURCE_LANG", "en")
DEFAULT_TARGET_LANG = os.getenv("TRANSLATE_TARGET_LANG", "es")
DEFAULT_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "my-gcp-project")


def get_translation_client() -> TranslationServiceClient:
    """Create and return a Google Cloud Translation v3 service client.

    Returns:
        Configured TranslationServiceClient instance.
    """
    return TranslationServiceClient()


def translate_text(
    text: str,
    target_language_code: str = DEFAULT_TARGET_LANG,
    source_language_code: str | None = None,
    project_id: str | None = None,
    client: TranslationServiceClient | None = None,
) -> dict[str, Any]:
    """Translate a single text string using Google Cloud Translation API v3.

    Uses the translate_v3 TranslationServiceClient to translate text from
    a source language to a target language.

    Args:
        text: The text string to translate.
        target_language_code: BCP-47 language code for the target language (e.g., 'es').
        source_language_code: BCP-47 language code for source language. Auto-detects if None.
        project_id: GCP project ID. Uses default if not provided.
        client: Optional pre-configured TranslationServiceClient.

    Returns:
        Dictionary with translated_text, source_language, and target_language.

    Raises:
        Exception: If the translation API call fails.
    """
    translator = client or get_translation_client()
    pid = project_id or DEFAULT_PROJECT_ID
    parent = f"projects/{pid}"

    request = {
        "parent": parent,
        "contents": [text],
        "target_language_code": target_language_code,
    }

    if source_language_code:
        request["source_language_code"] = source_language_code

    response = translator.translate_text(request=request)

    translated = response.translations[0].translated_text
    detected_source = response.translations[0].detected_language_code

    return {
        "translated_text": translated,
        "source_language": detected_source,
        "target_language": target_language_code,
        "original_text": text,
    }


def translate_payload_fields(
    payload: dict[str, Any],
    target_language_code: str = DEFAULT_TARGET_LANG,
    text_fields: list[str] | None = None,
    project_id: str | None = None,
    client: TranslationServiceClient | None = None,
) -> dict[str, Any]:
    """Translate specific text fields within a message payload.

    Extracts text from specified fields, translates them, and returns
    a new payload with translated values.

    Args:
        payload: The message payload dictionary.
        target_language_code: BCP-47 target language code.
        text_fields: List of field names to translate. Defaults to common fields.
        project_id: GCP project ID.
        client: Optional pre-configured TranslationServiceClient.

    Returns:
        New dictionary with translated text fields preserved.
    """
    if text_fields is None:
        text_fields = [
            "text", "message", "content", "description",
            "body", "comment", "subject", "title", "name",
        ]

    translator = client or get_translation_client()
    pid = project_id or DEFAULT_PROJECT_ID
    parent = f"projects/{pid}"

    texts_to_translate = []
    field_map = []

    for field_name in text_fields:
        value = payload.get(field_name)
        if value and isinstance(value, str):
            texts_to_translate.append(value)
            field_map.append(field_name)

    if not texts_to_translate:
        return dict(payload)

    request = {
        "parent": parent,
        "contents": texts_to_translate,
        "target_language_code": target_language_code,
    }

    response = translator.translate_text(request=request)

    translated_payload = dict(payload)
    for idx, field_name in enumerate(field_map):
        translated_payload[field_name] = response.translations[idx].translated_text

    return translated_payload


def translate_batch_texts(
    texts: list[str],
    target_language_code: str = DEFAULT_TARGET_LANG,
    source_language_code: str | None = None,
    project_id: str | None = None,
    client: TranslationServiceClient | None = None,
) -> list[dict[str, Any]]:
    """Translate a batch of texts in a single Google Cloud Translation API call.

    Args:
        texts: List of text strings to translate.
        target_language_code: BCP-47 target language code.
        source_language_code: BCP-47 source language code. Auto-detects if None.
        project_id: GCP project ID.
        client: Optional pre-configured TranslationServiceClient.

    Returns:
        List of translation result dictionaries.
    """
    translator = client or get_translation_client()
    pid = project_id or DEFAULT_PROJECT_ID
    parent = f"projects/{pid}"

    request = {
        "parent": parent,
        "contents": texts,
        "target_language_code": target_language_code,
    }

    if source_language_code:
        request["source_language_code"] = source_language_code

    response = translator.translate_text(request=request)

    results = []
    for idx, translation in enumerate(response.translations):
        results.append({
            "translated_text": translation.translated_text,
            "source_language": translation.detected_language_code,
            "target_language": target_language_code,
            "original_text": texts[idx],
        })

    return results


if __name__ == "__main__":
    result = translate_text(
        text="Welcome to our service! Your order has been confirmed.",
        target_language_code="es",
    )
    print(f"Translated: {result['translated_text']}")
    print(f"Detected source: {result['source_language']}")
