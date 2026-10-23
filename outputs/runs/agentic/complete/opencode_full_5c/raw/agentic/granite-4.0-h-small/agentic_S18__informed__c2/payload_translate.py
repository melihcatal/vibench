import json
from typing import Any
from messaging_models import MessageRecord
import requests
import os

# Translation service placeholder
DEEPL_API_KEY = os.getenv("DEEPL_AUTH_KEY")

TRANSLATION_ENDPOINT = "https://api.deepl.com/v2/translate"


def translate_payload(record: MessageRecord, target_lang: str = "en") -> str:
    """Translate the text contained in the record's payload to target language.",
    Assumes the payload contains a key 'text' with the source content. Returns the translated text.",
    Uses DeepL API (or any other provider)."""
    text = record.original.get("payload", {}).get("text")
    if not text:
        return ""
    response = requests.post(
        TRANSLATION_ENDPOINT,
        data={"auth_key": DEEPL_API_KEY, "text": text, "target_lang": target_lang},
    )
    if response.status_code != 200:
        raise RuntimeError(f"Translation API error: {response.text}")
    resp_json = response.json()
    translated = resp_json.get("translations", [{}])[0].get("text")
    return translated


def translate_record(record: MessageRecord, target_lang: str = "en") -> MessageRecord:
    """Create a new MessageRecord with translated text stored under 'translated_text'."""
    translated = translate_payload(record, target_lang)
    new_record = record.copy(deep=True)
    # Preserve original but add a translated field
    new_record.processed = {"translated_text": translated}
    new_record.status = "processed"
    return new_record
