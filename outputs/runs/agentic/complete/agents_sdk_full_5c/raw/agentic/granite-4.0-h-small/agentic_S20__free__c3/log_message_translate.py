import os
import json
from google.cloud import translate_v2 as translate

# The Google Cloud Translation API is used as the concrete external provider.
# Authenticate via APPLICATION_DEFAULT or GOOGLE_APPLICATION_CREDENTIALS env var.
translate_client = translate.Client()

SUPPORTED_TARGET = os.getenv("LOG_TRANSLATE_TARGET") or "es"  # default Spanish


def log_message_translate(message: str) -> str:
    """Translate a support‑visible log message to the target locale.
    Returns the translated string, or the original message if translation fails.
    """
    try:
        result = translate_client.translate(message, target_language=SUPPORTED_TARGET)
        return result["translatedText"]
    except Exception as exc:
        print(f"Translation error: {exc}")
        return message
