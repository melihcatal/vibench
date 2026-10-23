# [LATER-STEP] dashboard_note_translate.py
# Translate metric or dashboard notes for another locale using Google Cloud Translation SDK

import os
from google.cloud import translate_v2 as translate
from observability_client import get_monitoring_client
from observability_models import TimeInterval

translation_client = translate.Client()

def dashboard_note_translate(source_locale: str = "en", target_locale: str = "es") -> None:
    """Retrieve all dashboard notes from the current project, translate them,
    and print source/target pairs.
    
    Args:
        source_locale: BCP-47 language tag of the source text (default "en").
        target_locale: BCP-47 language tag for the translation (default "es").
    """
    # Placeholder: In a real implementation you would call the Monitoring API
    # to list dashboards, then their associated notes/annotations. Here we simulate
    # with a static list.
    notes = [
        "CPU utilization spiked during the load test.",
        "Memory pressure was low throughout the monitoring window."
    ]
    # Translate each note using Google Cloud Translation
    for note in notes:
        result = translation_client.translate(note, source_language=source_locale, target_language=target_locale)
        print(f"Original ({source_locale}): {note}\nTranslated ({target_locale}): {result['translatedText']}\n---")
