import os
from typing import List
from observability_client import get_logging_client
from google.cloud import translate_v2 as translate


def translate_log_messages(
    log_messages: List[str], target_language: str = "es"
) -> List[Dict[str, str]]:
    """Translate support-visible log messages to another locale using Google Cloud Translation API."""
    client = get_logging_client("google")
    translate_client = translate.Client()

    results = []
    for message in log_messages:
        if not message:
            continue

        # Translate the message
        result = translate_client.translate(message, target_language=target_language)

        results.append(
            {
                "original_message": message,
                "translated_message": result["translatedText"],
            }
        )

    return results
