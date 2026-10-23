import os
from typing import Dict
from observability_client import get_translation_client


def translate_log_messages(
    messages: List[str], target_locale: str = "es"
) -> List[Dict[str, str]]:
    """Translates support‑visible log messages for another locale.

    Args:
        messages: List of original log message strings.
        target_locale: Destination language code (e.g., "es", "fr").

    Returns a list of dictionaries mapping the original message to its translation.
    Uses Google Cloud Translation as the concrete provider (identified by the SDK import)."""
    client = (
        get_translation_client()
    )  # Google Cloud Translation client configured via env vars
    responses = []
    # Translation API accepts up to 128 messages per request; batch if needed
    for batch in [messages[i : i + 128] for i in range(0, len(messages), 128)]:
        translation = client.translate(batch, target_language=target_locale)
        for src, trg in zip(batch, translation):
            responses.append({"original": src, "translated": trg})
    return responses
