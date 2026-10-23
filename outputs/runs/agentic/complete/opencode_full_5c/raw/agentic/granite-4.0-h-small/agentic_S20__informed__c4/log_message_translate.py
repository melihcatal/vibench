import os
import requests
from observability_models import LogEvent


def log_message_translate(log_event: LogEvent, target_locale: str = "es") -> str:
    """Translate support‑visible log messages for another locale using Google Cloud Translation API.

    Returns the translated message string.
    """
    api_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
        )

    from google.cloud import translate_v2 as translate

    client = translate.Client()

    try:
        translation = client.translate(log_event.message, target_language=target_locale)
        return translation["translatedText"]
    except Exception as e:
        print(f"Translation failed: {e}")
        return log_event.message  # fallback to original message
