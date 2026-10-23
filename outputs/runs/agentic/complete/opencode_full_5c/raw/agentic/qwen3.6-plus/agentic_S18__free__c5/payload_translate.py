import os
import json
from typing import Dict, Any, Optional, List
from google.cloud import translate_v2 as translate
from messaging_models import normalize_payload, extract_text_from_payload


def translate_message_payload(
    message_data: Dict[str, Any],
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "my-gcp-project")
    client = translate.Client()

    payload = normalize_payload(message_data.get("data", message_data))
    text = extract_text_from_payload(payload)

    if not text or len(text.strip()) == 0:
        return {
            "original_text": "",
            "translated_text": "",
            "source_language": "unknown",
            "target_language": target_language,
            "message_id": message_data.get("message_id", "unknown"),
            "provider": "google-cloud-translate",
            "model": "nmt",
            "status": "no_content",
        }

    translate_kwargs = {
        "q": text,
        "target_language": target_language,
        "format_": "text",
    }

    if source_language:
        translate_kwargs["source_language"] = source_language

    result = client.translate(**translate_kwargs)

    translated_text = result.get("translatedText", text)
    detected_source = result.get("detectedSourceLanguage", source_language or "unknown")

    return {
        "original_text": text,
        "translated_text": translated_text,
        "source_language": detected_source,
        "target_language": target_language,
        "message_id": message_data.get("message_id", "unknown"),
        "provider": "google-cloud-translate",
        "model": "nmt",
        "status": "translated",
    }


def batch_translate_payloads(
    messages: List[Dict[str, Any]],
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    results = []

    for msg in messages:
        translation = translate_message_payload(msg, target_language, source_language)
        results.append(translation)

    return {
        "translations": results,
        "total_translated": len(results),
        "target_language": target_language,
        "provider": "google-cloud-translate",
        "model": "nmt",
    }


if __name__ == "__main__":
    sample_message = {
        "message_id": "msg_translate_001",
        "data": {"text": "Bonjour, comment allez-vous aujourd'hui?"},
    }
    result = translate_message_payload(sample_message, target_language="en")
    print(json.dumps(result, indent=2))
