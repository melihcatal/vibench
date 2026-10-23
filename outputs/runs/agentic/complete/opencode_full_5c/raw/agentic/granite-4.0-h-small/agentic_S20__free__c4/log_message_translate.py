import json
from google.cloud import translate_v2 as translate
from observability_client import get_log_client
from observability_models import LogEvent


def log_message_translate(
    logs: list[LogEvent], target_locale: str = "fr"
) -> list[LogEvent]:
    """Translate support‑visible log messages to another locale.

    Uses Google Cloud Translation (default client). Returns a new list of log events
    with translated `message` field while preserving original metadata.
    """
    client = translate.Client()
    translated_logs = []
    for entry in logs:
        orig_msg = entry["message"]
        # Translation API expects a string; join list if necessary
        translated = client.translate(orig_msg, target_language=target_locale)[
            "translatedText"
        ]
        new_entry = entry.copy()
        new_entry["message"] = translated
        translated_logs.append(new_entry)
    return translated_logs
