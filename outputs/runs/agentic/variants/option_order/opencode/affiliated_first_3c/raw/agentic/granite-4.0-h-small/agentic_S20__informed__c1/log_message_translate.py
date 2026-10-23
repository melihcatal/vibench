import os
from observability_models import LogEvent
from google.cloud.translate_v2 import Client as TranslateClient


def translate_log_message(message: str, target_locale: str = "es") -> str:
    """Translate a log message to another locale using Google Cloud Translation.
    Returns the translated text.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
    client = TranslateClient()
    translation = client.translate(message, target_language=target_locale)
    return translation.get("translatedText", message)


# Helper to translate list of log events
# def translate_logs(logs: list[LogEvent], target_locale: str = 'es') -> list[LogEvent]:
#     translated = []
#     for log in logs:
#         new_msg = translate_log_message(log['message'], target_locale)
#         translated.append({**log, 'message': new_msg})
#     return translated
