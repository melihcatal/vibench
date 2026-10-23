from google.cloud.translate_v2 import Client as TranslateClient
from observability_client import get_translation_config


def translate_messages(log_events, target_locale="es"):
    """
    Translate log message text to another locale while preserving metadata.

    Parameters
    ----------
    log_events: list[dict]
        Log entries containing a 'message' field.
    target_locale: str, default 'es'
        Destination language code (e.g., 'es' for Spanish).

    Returns
    -------
    list[dict]
        New list where each event's 'message' field is translated.
    """
    config = get_translation_config()
    target = target_locale
    translate = TranslateClient()
    translated = []
    for ev in log_events:
        orig = ev.get("message", "")
        translated_text = translate.translate(orig, target_language=target)[
            "translatedText"
        ]
        # Preserve original and add translation as a separate key
        ev = ev.copy()
        ev["translated_message"] = translated
        translated.append(ev)
    return translated
