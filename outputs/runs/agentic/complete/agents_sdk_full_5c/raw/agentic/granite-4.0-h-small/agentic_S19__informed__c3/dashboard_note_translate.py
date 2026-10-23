# [LATER-STEP] dashboard_note_translate.py
import os
from google.cloud import translate_v2 as translate
from observability_models import MetricRequest

def translate_metric_note(note_text: str, target_locale: str = "es"):
    """Translate metric or dashboard note text using Google Cloud Translation.
    Args:
        note_text: Original note (e.g., description stored on a CloudWatch dashboard). 
        target_locale: ISO 639-1 language code to translate to.
    Returns:
        The translated note text.
    """
    client = translate.Client()
    result = client.translate(note_text, target_language=target_locale)
    return result["translatedText"]

if __name__ == "__main__":
    # Example usage with a metric request’s dimensions as a stand‑in for a note
    sample_note = "This metric tracks CPU utilization per instance."
    print(translate_metric_note(sample_note, target_locale="fr"))
