import os
from typing import Optional
from observability_models import LogEvent

def translate_message(message: str, target_locale: str) -> str:
    """Translate a log message to another locale using Google Cloud Translation.

    Returns the translated string. Raises RuntimeError if credentials are missing.
    """
    from google.cloud import translate_v2 as translate
    creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds:
        raise RuntimeError('Missing GOOGLE_APPLICATION_CREDENTIALS env var')
    client = translate.Client()
    result = client.translate(message, target_language=target_locale)
    return result['translatedText']


def translate_log_event(event: LogEvent, target_locale: str) -> LogEvent:
    """Create a copy of the log event with the message translated.

    The original metadata and request_id are preserved.
    """
    translated_msg = translate_message(event.message, target_locale)
    return LogEvent(
        message=translated_msg,
        event_type=event.event_type,
        level=event.level,
        request_id=event.request_id,
        timestamp=event.timestamp,
        metadata=event.metadata
    )
