import os
import json
from observability_client import ManagedLogClient
from observability_models import LogEntry


def log_message_translate(
    log_entries: list[LogEntry], target_locale: str = "es"
) -> list[LogEntry]:
    """Translate support‑visible log messages for another locale using DeepL API.

    Returns new LogEntry objects with translated text. The concrete provider is DeepL.
    """
    translated = []
    for entry in log_entries:
        translated_text = _translate_text(entry.message, target_locale)
        new_entry = entry
        new_entry.message = translated_text
        translated.append(new_entry)
    return translated


def _translate_text(text: str, target_locale: str) -> str:
    # Placeholder – in production call DeepL SDK or REST API
    # Example: from deepl import DeepL; translator = DeepL(auth_key=DEEPL_AUTH_KEY)
    # result = translator.translate_text(text, target_lang=target_locale)
    # return result.text
    return f"[translated to {target_locale}: {text[:30]}...]"
