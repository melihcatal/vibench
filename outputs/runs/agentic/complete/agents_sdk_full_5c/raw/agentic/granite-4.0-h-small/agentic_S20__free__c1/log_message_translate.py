import json
from google.cloud import translate_v2 as translate
from observability_models import LogEvent

# Using Google Cloud Translation API as the concrete provider (model identifier is implicit)

def log_message_translate(log_event: LogEvent, target_locale: str = "es") -> LogEvent:
    """Translate the message field of a log event into another locale.

    Args:
        log_event (LogEvent): Original log entry.
        target_locale (str): Destination locale code (default 'es' for Spanish).

    Returns:
        LogEvent: New entry with translated message.
    """
    client = translate.Client()
    original_msg = log_event.get('message', '')
    if not original_msg:
        return log_event  # nothing to translate
    # Translate using Google Cloud Translation model
    translation = client.translate(original_msg, target_language=target_locale)['translatedText']
    # Return a new normalized dict
    translated_event = {
        'timestamp': log_event['timestamp'],
        'level': log_event['level'],
        'message': translation,
        'source': log_event.get('source', 'unknown'),
        'extra': log_event.get('extra', {})
    }
    return translated_event
