# Translate metric or dashboard notes for another locale using DeepL API.

import os
from .observability_client import init_client
from .observability_models import normalize_datadog_points

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")

import deepl

translator = deepl.Translator(DEEPL_AUTH_KEY)
LANGUAGE_TARGET = "DE"  # German, change as needed

METRIC_NOTE = "CPU usage spikes are expected during batch jobs."


def dashboard_note_translate(note: str) -> str:
    """Translate a single note string into the target locale."""
    result = translator.translate_text(text=note, target_lang=LANGUAGE_TARGET)
    return result.text


if __name__ == "__main__":
    translation = dashboard_note_translate(METRIC_NOTE)
    print(f"Original: {METRIC_NOTE}\nTranslated: {translation}")

# ---------------------------------------------------------------------------
# To translate multiple notes, call dashboard_note_translate() for each.
# ---------------------------------------------------------------------------
