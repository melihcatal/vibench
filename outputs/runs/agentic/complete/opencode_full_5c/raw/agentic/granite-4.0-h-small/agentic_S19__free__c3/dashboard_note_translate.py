# LATER-STEP
# dashboard_note_translate.py
# Translate metric or dashboard notes to another locale using a language translation SaaS (DeepL as example)

import os
from deepl import DeepL, TranslateParams
from observability_client import get_datadog_client
from observability_models import MetricQueryRequest, MetricQueryResponse


def translate_note(note_text: str, target_lang: str = "es") -> str:
    """
    Translate a free‑text note (metric annotation or dashboard description) to the target language.

    Args:
        note_text (str): Original note string.
        target_lang (str): ISO language code, e.g., "es" for Spanish, "fr" for French.

    Returns:
        str: Translated note.
    """
    # Initiate DeepL client using env var DEEPL_AUTH_KEY
    deepl = DeepL(auth_key=os.getenv("DEEPL_AUTH_KEY"))
    if not deepl:
        raise RuntimeError("DEEPL_AUTH_KEY not configured")
    params = TranslateParams(
        text=note_text,
        target_lang=target_lang,
        # Optionally set formality, glossary, etc.
    )
    result = deepl.translate(params)  # DeepL SDK call
    return result.translated_text


def translate_dashboard_notes(dashboard_id: str, target_lang: str = "fr") -> None:
    """
    Example helper that fetches notes for a dashboard and writes back translated versions.
    This file demonstrates the workflow; integration with Datadog's Dashboard API would replace the placeholder.
    """
    client = get_datadog_client()
    # Placeholder: imagine client.dashboard_notes(...) returns a list of note dicts
    notes = []  # replace with real API call
    for note in notes:
        translated = translate_note(note["text"], target_lang)
        print(f"Original: {note['text']} => Translated: {translated}")
