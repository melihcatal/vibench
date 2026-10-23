import os
from observability_client import ObservabilityClient, MetricResponse


def translate_dashboard_note(note_text, target_locale="en"):
    """Translate metric or dashboard notes for another locale.

    Args:
        note_text (str): Original note text.
        target_locale (str): ISO code for the target language.

    Returns:
        str: Translated note.
    """
    client = ObservabilityClient()
    payload = {"text": note_text, "target": target_locale}
    response = client.rest_call(method="POST", endpoint="/v1/translate", json=payload)
    normalized = MetricResponse.from_raw(response)
    if normalized.status != "ok":
        return f"Translation error: {normalized.message}"
    return normalized.data.get("translatedText", note_text)
