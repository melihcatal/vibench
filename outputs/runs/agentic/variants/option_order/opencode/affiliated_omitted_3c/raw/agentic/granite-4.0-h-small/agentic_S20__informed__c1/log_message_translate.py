import os
from observability_client import get_query_client
from observability_models import LogEvent
import requests


def translate_log_messages(
    events: list[LogEvent], target_locale: str = "es"
) -> list[LogEvent]:
    """Translates support‑visible log messages for another locale.

    Uses Google Cloud Translation API (or another provider) as an example.
    The function adds a new field `translated_message` to each event and returns
    the updated list. In a real integration you would map the provider's SDK.
    """
    # --- Example: Google Cloud Translation -----------------------------------
    # You must set GOOGLE_APPLICATION_CREDENTIALS env var for credentials.
    from google.cloud import translate_v2 as translate

    client = translate.Client()
    translated_events = []
    for evt in events:
        original = evt["message"]
        # Translate text while preserving newlines for readability
        translation = client.translate(original, target_language=target_locale)[
            "translatedText"
        ]
        new_evt = evt.copy()
        new_evt["translated_message"] = translation
        translated_events.append(new_evt)
    return translated_events
