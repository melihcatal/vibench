import os
import json
import requests
from typing import Dict

# Alibaba Machine Translation endpoint and key
ALIBABA_MT_URL = "https://api-jssmart.alipayobjects.com/api/mt/translate"
ALIBABA_MT_KEY = os.getenv("ALIBABA_MT_KEY")
if not ALIBABA_MT_KEY:
    raise RuntimeError("ALIBABA_MT_KEY environment variable not set")

HEADERS = {
    "Content-Type": "application/json",
    "x-acs-signature-nonce": "unique-123",  # simplified; real requests use signing
    "x-acs-key-id": ALIBABA_MT_KEY,
    "x-acs-version": "2018-01-11",
}


def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate `text` into `target_lang` using Alibaba Machine Translation.

    Returns the translated string.
    """
    payload = {
        "src_lang": "auto",
        "target_lang": target_lang,
        "content": text,
    }
    response = requests.post(ALIBABA_MT_URL, json=payload, headers=HEADERS)
    if response.status_code != 200:
        raise RuntimeError(f"Translation API failed: {response.status_code} {response.text}")
    result = response.json()
    # Alibaba response format: {"translated": "..."}
    return result.get("translated", text)


def enrich_event(event: Dict) -> Dict:
    """Add a translated version of any customer‑facing payload text.

    The function looks for a key `customer_message` under `event['payload']` and,
    if present, adds a `translated` field with the target language set to English.
    """
    payload = event.get("payload", {})
    customer_message = payload.get("customer_message")
    if customer_message:
        payload["translated"] = translate_text(customer_message)
    return event
