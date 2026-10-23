"""Translate customer-facing message payload text using Azure AI Translator.

Uses the Azure AI Translator REST API to translate text in message
payloads. Authentication relies on AZURE_TRANSLATOR_KEY and
AZURE_TRANSLATOR_REGION.
"""

import os
import json
from typing import Dict, List, Optional

import requests

from messaging_models import ConsumedMessage


TRANSLATOR_ENDPOINT = os.environ.get(
    "AZURE_TRANSLATOR_ENDPOINT",
    "https://api.cognitive.microsofttranslator.com",
)
TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY", "")
TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION", "global")


def translate_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> str:
    """Translate a single text string via Azure AI Translator.

    Args:
        text: The source text to translate.
        target_language: ISO 639-1 language code to translate into.
        source_language: Optional ISO 639-1 source language code.

    Returns:
        Translated text string.
    """
    url = f"{TRANSLATOR_ENDPOINT.rstrip('/')}/translate"

    params: Dict[str, str] = {
        "api-version": "3.0",
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION,
        "Content-Type": "application/json",
    }

    body = [{"text": text}]

    response = requests.post(url, params=params, headers=headers, json=body, timeout=15)
    response.raise_for_status()

    result = response.json()
    translations = result[0].get("translations", [])
    if translations:
        return translations[0].get("text", text)
    return text


def translate_message_payload(
    message: ConsumedMessage,
    target_language: str = "en",
    text_fields: Optional[List[str]] = None,
) -> Dict[str, str]:
    """Translate string-valued fields in a message payload.

    Args:
        message: The consumed message whose payload contains text to translate.
        target_language: Target ISO 639-1 language code.
        text_fields: Optional list of payload keys to translate (all string fields if None).

    Returns:
        Dict mapping each field name to its translated text.
    """
    payload = message.payload
    if not text_fields:
        text_fields = [k for k, v in payload.items() if isinstance(v, str)]

    translations: Dict[str, str] = {}
    for field_name in text_fields:
        original = payload.get(field_name, "")
        if not original or not isinstance(original, str):
            continue
        translated = translate_text(original, target_language=target_language)
        translations[field_name] = translated

    return translations


def translate_and_attach(
    message: ConsumedMessage,
    target_language: str = "en",
    text_fields: Optional[List[str]] = None,
) -> str:
    """Translate payload text fields and return a combined translated string.

    Args:
        message: The consumed message.
        target_language: Target language code.
        text_fields: Fields to translate.

    Returns:
        Combined translated text from all specified fields joined by newlines.
    """
    translations = translate_message_payload(
        message,
        target_language=target_language,
        text_fields=text_fields,
    )
    if not translations:
        return ""
    return "\n".join(translations.values())


if __name__ == "__main__":
    sample = ConsumedMessage(
        message_id="msg-tl-1",
        event_id="evt-tl-001",
        event_type="feedback.received",
        source="support-api",
        payload={"feedback": "Muy buen servicio, gracias.", "author": "carlos"},
        attributes={},
    )
    translated = translate_and_attach(sample, target_language="en")
    print(json.dumps({"translation": translated}))
