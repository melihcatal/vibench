from google.cloud import translate_v2 as translate
import json
from typing import Dict, Any


def translate_payload(
    msg: Dict[str, Any], target_language: str = "es"
) -> Dict[str, Any]:
    """
    Translates customer-facing message payload text using Google Translate.
    """
    client = translate.Client()
    payload = msg.get("payload", {})
    translated_payload = {}
    for key, value in payload.items():
        if isinstance(value, str) and value.strip():
            result = client.translate(value, target_language=target_language)
            translated_payload[key] = result["translatedText"]
        else:
            translated_payload[key] = value
    return {**msg, "payload": translated_payload}
