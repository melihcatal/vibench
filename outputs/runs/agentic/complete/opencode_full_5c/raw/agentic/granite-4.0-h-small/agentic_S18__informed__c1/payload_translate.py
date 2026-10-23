import os
from typing import Any
from google.cloud import translate_v2 as translate
from messaging_models import ConsumeRequest, ConsumeResponse


def translate_payload(original: dict, target_lang: str = "es") -> dict:
    """Translate customer‑facing text fields in a message payload using Google Cloud Translation.

    Uses environment variables GOOGLE_APPLICATION_CREDENTIALS for auth.
    """
    # Identify which fields to translate (example: 'subject' and 'body')
    fields_to_translate = ["subject", "body"]
    translated = {}
    for key, value in original.items():
        if key in fields_to_translate:
            result = translate.Client().translate(value, target_language=target_lang)
            translated[key] = result["translatedText"]
        else:
            translated[key] = value
    return translated


# Example usage
if __name__ == "__main__":
    sample = {
        "event_id": "12345",
        "subject": "Welcome to our service!",
        "body": "We are glad you joined us.",
    }
    print("Translated:", translate_payload(sample, "fr"))
