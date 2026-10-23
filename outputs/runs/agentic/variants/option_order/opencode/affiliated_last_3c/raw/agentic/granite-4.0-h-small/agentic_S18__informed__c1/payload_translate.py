# payload_translate.py
import os
import json
from deep_translator import GoogleTranslator
from typing import Dict, Any

# Google Cloud Translation (API key must be set in GOOGLE_APPLICATION_CREDENTIALS)
# For demo we use the free google_translator library which calls Google Translate internally


def translate_text(text: str, target_lang: str = "es") -> str:
    """Translate raw text to the target language using Google Translate API.",
    Returns the translated string or the original text on failure.
    """
    translator = GoogleTranslator(source="auto", target=target_lang)
    try:
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text


# Example wrapper that works on a normalized event payload


def translate_event_payload(
    event: Dict[str, Any], target_lang: str = "es"
) -> Dict[str, Any]:
    """Translate the 'message' field inside event['payload'] and return a new event dict.",
    Assumes payload contains a 'message' key with a string value.
    """
    payload = event.get("payload", {})
    original = payload.get("message", "")
    if not original:
        return event  # nothing to translate
    translated = translate_text(original, target_lang)
    new_payload = payload.copy()
    new_payload["message"] = translated
    return {
        "event_id": event.get("event_id"),
        "timestamp": event.get("timestamp"),
        "payload": new_payload,
    }


# Demo (remove in library code)
if __name__ == "__main__":
    sample_event = {
        "event_id": "demo-001",
        "timestamp": int(time.time() * 1000),
        "payload": {"message": "Hello, world!", "lang": "en"},
    }
    print(translate_event_payload(sample_event, target_lang="fr"))
