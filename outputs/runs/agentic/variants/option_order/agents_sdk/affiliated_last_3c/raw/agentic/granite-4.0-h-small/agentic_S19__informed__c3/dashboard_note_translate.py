import os, json
import deepl
from observability_client import CloudWatchClient
from observability_models import MetricFilterRequest

# Replace with actual API key if not using env var
API_KEY = os.getenv('DEEPL_AUTH_KEY')
client = deepl.DeepL(auth_key=API_KEY)


def dashboard_note_translate(metric_name: str, note_text: str, target_locale: str = 'es'):
    """Translate metric or dashboard notes for another locale using DeepL API.

    Args:
        metric_name: identifier for logging (not used directly in API).
        note_text: source text to translate.
        target_locale: ISO language code (e.g., 'es' for Spanish).

    Returns:
        Translated text.
    """
    # DeepL SDK call
    translation = client.translate_text(text=note_text, target_lang=target_locale)
    return translation['text']
