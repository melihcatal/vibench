import os
import boto3  # Amazon Translate integration (or Google Cloud Translation if preferred)
from typing import Dict, Any

# Translation target language (ISO 639-1, e.g., 'es' for Spanish)
TARGET_LANG = os.getenv("TRANSLATION_TARGET", "es")

# Initialise Translate client (AWS region can be set via env var)
translate = boto3.client("translate", region_name="us-east-1")


def translate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Translate the 'text' field of a payload to TARGET_LANG using Amazon Translate."""
    original = payload.get("text", "")
    if not original:
        return payload  # Nothing to translate
    response = translate.translate_text(
        Text=original, SourceLanguageCode="en", TargetLanguageCode=TARGET_LANG
    )
    translated = response.get("TranslatedText", "")
    # Return a new payload with both original and translated text
    new_payload = payload.copy()
    new_payload["translated_text"] = translated
    return new_payload


# Batch translation helper


def batch_translate(payloads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [translate_payload(p) for p in payloads]


# Example usage
if __name__ == "__main__":
    sample = {"id": "msg-001", "text": "Hello, how are you?"}
    translated = translate_payload(sample)
    print("Original:", sample["text"])
    print("Translated:", translated["translated_text"])
