# payload_translate.py
# [LATER-STEP]
# Translate customer‑facing message payload text using Google Cloud Translation API

import os
import google.cloud.translate_v2 as translate
from messaging_models import deserialize_message, serialize_message


def translate_payload(message: dict, target_lang: str = "es") -> dict:
    """Translate the *text* field inside the message payload.

    Args:
        message (dict): Normalized message with a 'payload' containing a 'text' key.
        target_lang (str): ISO language code, default 'es' (Spanish).

    Returns:
        dict: Same message dict with the translated text replacing the original.
    """
    # Ensure API key is set in environment
    api_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not api_key:
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS not set")

    client = translate.Client()
    payload = message.get("payload", {})
    if "text" not in payload:
        # No text field to translate; return unchanged
        return message
    original = payload["text"]
    # Call the translation API
    result = client.translate(original, target_language=target_lang)
    payload["text"] = result["translatedText"]
    return message


if __name__ == "__main__":
    # Tiny CLI demo: pass a JSON file with a message, output translated version
    import sys, json

    if len(sys.argv) != 2:
        print("Usage: python payload_translate.py <message.json>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        msg = json.load(f)
    translated = translate_payload(msg)
    print(json.dumps(translated, indent=2))
