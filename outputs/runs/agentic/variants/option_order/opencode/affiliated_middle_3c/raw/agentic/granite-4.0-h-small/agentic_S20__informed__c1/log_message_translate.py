from google.cloud import translate_v2 as translate


def log_message_translate(messages: list, target_locale: str = "es") -> list:
    """Translates support‑visible log messages to another locale.

    Uses Google Cloud Translation API. Replace with another provider
    if desired, keeping the same function signature.

    Args:
        messages (list): List of log dicts containing a 'text' field.
        target_locale (str): ISO locale code (e.g., 'es', 'fr').

    Returns:
        list: Translated log dicts with an added 'translated_text' field.
    """
    translate_client = translate.Client()
    translated = []
    for msg in messages:
        orig = msg.get("text", "")
        if not orig:
            translated.append(msg)
            continue
        result = translate_client.translate(orig, target_language=target_locale)
        msg = msg.copy()
        msg["translated_text"] = result["translatedText"]
        translated.append(msg)
    return translated
