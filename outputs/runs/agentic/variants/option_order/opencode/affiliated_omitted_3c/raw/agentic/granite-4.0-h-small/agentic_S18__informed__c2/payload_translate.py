import os
import requests
from typing import Any, Dict
from messaging_models import PublishRequest

TRANSLATE_ENDPOINT = os.getenv("ALIBABA_ALIMT_ENDPOINT", "https://mt.aliyuncs.com")
TRANSLATE_KEY = os.getenv("ALIBABA_ALIMT_KEY")

CLOUD_PLATFORM = "aliyun"
TARGET_LANG = "en"

TRANSLATION_MAPPING: Dict[str, str] = {
    CLOUD_PLATFORM: {
        "topic": "topic",
    },
}


def translate_payload(
    request: PublishRequest, cloud_provider: str = CLOUD_PLATFORM
) -> PublishRequest:
    """Translate customer‑facing text fields in the payload using Alibaba Cloud Translation."""
    if not TRANSLATE_ENDPOINT or not TRANSLATE_KEY:
        print("Translation credentials not configured, skipping translation.")
        return request
    payload = request["event_data"]
    text_fields = ["text", "title", "description"]
    for field in text_fields:
        if field in payload and isinstance(payload[field], str):
            src_text = payload[field]
            # Call Alibaba Cloud Machine Translation (simplified mock)
            translated = _mock_translate(src_text, target_lang=TARGET_LANG)
            payload[field] = translated
    # Return a new request with translation applied (immutable style)
    return {
        **request,
        "event_data": payload,
    }


def _mock_translate(text: str, target_lang: str = TARGET_LANG) -> str:
    """Stub for Alibaba Cloud Translation API call."""
    # In production replace this with a real API request (e.g., using alibabacloud_alimt SDK)
    return f"[Translated({target_lang})]: {text}"
