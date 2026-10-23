"""
[LATER-STEP] Translate customer-facing message payload text using Google Cloud Translation API.
Provider: Google Cloud Translation
SDK: google-cloud-translate
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import os
from typing import Optional, List
from messaging_models import PubSubEvent, extract_text_from_event


def translate_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
) -> str:
    """
    Translate text using Google Cloud Translation API v2.

    Args:
        text: The text to translate.
        target_language: Target language code (e.g., 'en', 'es', 'fr').
        source_language: Source language code. None for auto-detection.
        project_id: Google Cloud project ID.

    Returns:
        The translated text string.
    """
    from google.cloud import translate_v2 as translate

    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")
    client = translate.Client(project=project_id)

    kwargs = {"target_language": target_language}
    if source_language:
        kwargs["source_language"] = source_language

    result = client.translate(text, **kwargs)
    return result["translatedText"]


def translate_event_payload(
    event: PubSubEvent,
    target_language: str = "en",
    project_id: Optional[str] = None,
) -> str:
    """
    Extract and translate text from a PubSubEvent payload.

    Args:
        event: The PubSubEvent containing text to translate.
        target_language: Target language code.
        project_id: Google Cloud project ID.

    Returns:
        The translated text.
    """
    text = extract_text_from_event(event)
    return translate_text(text, target_language=target_language, project_id=project_id)


def translate_batch(
    events: List[PubSubEvent],
    target_language: str = "en",
    project_id: Optional[str] = None,
) -> dict:
    """
    Translate payloads from multiple events.

    Args:
        events: List of PubSubEvent objects.
        target_language: Target language code.
        project_id: Google Cloud project ID.

    Returns:
        Dictionary mapping event IDs to translated text.
    """
    translations = {}
    for event in events:
        translated = translate_event_payload(event, target_language, project_id)
        translations[event.event_id] = translated
    return translations
