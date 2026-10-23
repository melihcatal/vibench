"""Translate customer-facing message payload text using DeepL API.

Uses the deepl SDK to translate message payloads between supported languages
for international customer communications.
"""

import os
import json
from typing import Optional, Dict, Any, List

import deepl


def translate_payload(
    text: str,
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Translate message payload text using DeepL Translation API.

    Args:
        text: Text content to translate.
        target_lang: Target language code (e.g., "EN-US", "DE", "FR", "ES").
        source_lang: Source language code. Auto-detected if not provided.
        api_key: DeepL API key. Falls back to DEEPL_API_KEY env var.

    Returns:
        Dict with translated text and metadata.
    """
    if api_key is None:
        api_key = os.environ.get("DEEPL_API_KEY")

    translator = deepl.Translator(api_key)

    translate_kwargs = {
        "target_lang": target_lang,
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    result = translator.translate_text(text, **translate_kwargs)

    return {
        "status": "translated",
        "original_text": text,
        "translated_text": result.text,
        "source_language": result.detected_source_lang if hasattr(result, "detected_source_lang") else source_lang or "auto",
        "target_language": target_lang,
    }


def translate_message_payload(
    message_data: Dict[str, Any],
    target_lang: str = "EN-US",
    text_fields: Optional[List[str]] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Translate text fields within a message payload using DeepL.

    Args:
        message_data: Message dict containing payload to translate.
        target_lang: Target language code.
        text_fields: List of payload field names to translate.
            Defaults to ["text", "content", "message", "body"].
        api_key: DeepL API key.

    Returns:
        Dict with translated payload and metadata.
    """
    if api_key is None:
        api_key = os.environ.get("DEEPL_API_KEY")

    translator = deepl.Translator(api_key)

    if text_fields is None:
        text_fields = ["text", "content", "message", "body", "description"]

    payload = message_data.get("payload", message_data)
    translated_payload = dict(payload)
    translations = {}

    for field_name in text_fields:
        if field_name in payload and isinstance(payload[field_name], str):
            text_to_translate = payload[field_name]
            if text_to_translate.strip():
                result = translator.translate_text(
                    text_to_translate,
                    target_lang=target_lang,
                )
                translated_payload[field_name] = result.text
                translations[field_name] = {
                    "original": text_to_translate,
                    "translated": result.text,
                    "detected_source": getattr(result, "detected_source_lang", "unknown"),
                }

    return {
        "status": "translated",
        "target_language": target_lang,
        "original_payload": payload,
        "translated_payload": translated_payload,
        "translations": translations,
        "event_id": message_data.get("event_id", "unknown"),
    }


def batch_translate_payloads(
    messages: List[Dict[str, Any]],
    target_lang: str = "EN-US",
    text_field: str = "text",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Translate the same field across multiple messages using DeepL.

    Args:
        messages: List of message dicts to translate.
        target_lang: Target language code.
        text_field: Field name in each message payload to translate.
        api_key: DeepL API key.

    Returns:
        Dict with batch translation results.
    """
    if api_key is None:
        api_key = os.environ.get("DEEPL_API_KEY")

    translator = deepl.Translator(api_key)

    texts = []
    message_ids = []
    for msg in messages:
        payload = msg.get("payload", msg)
        text = payload.get(text_field, "")
        if text:
            texts.append(text)
            message_ids.append(msg.get("event_id", msg.get("message_id", "unknown")))

    if not texts:
        return {
            "status": "no_text_to_translate",
            "results": [],
            "target_language": target_lang,
        }

    # DeepL supports translating multiple texts in one call
    results = translator.translate_text(texts, target_lang=target_lang)

    translation_results = []
    for i, result in enumerate(results):
        translation_results.append({
            "message_id": message_ids[i] if i < len(message_ids) else f"index-{i}",
            "original": texts[i],
            "translated": result.text,
            "detected_source": getattr(result, "detected_source_lang", "unknown"),
        })

    return {
        "status": "batch_translated",
        "target_language": target_lang,
        "count": len(translation_results),
        "results": translation_results,
    }


if __name__ == "__main__":
    sample_text = "Votre commande #12345 a été expédiée et arrivera demain."
    result = translate_payload(sample_text, target_lang="EN-US")
    print(json.dumps(result, indent=2))
