import os
from observability_client import MonitoringClient
from observability_models import MetricQueryRequest
from google.cloud.translate_v2 import Client as TranslateClient

def dashboard_note_translate(metric_query: MetricQueryRequest, target_lang: str = 'es'):
    """Translate metric or dashboard notes for another locale using Google Cloud Translation.

    Requires env var: GOOGLE_APPLICATION_CREDENTIALS (or GOOGLE_TRANSLATE_CREDENTIALS)
    """
    # ----- Translation client -----
    translate = TranslateClient()

    # ----- Retrieve notes from metric (example: use a label called 'note') -----
    query = metric_query.to_dict()
    raw_points = MonitoringClient().fetch_time_series(query)
    notes = []
    for point in raw_points:
        for sample in point.points:
            val = sample.value.string_value
            if val and 'note' in sample.label:
                notes.append(val)
    if not notes:
        return {'status': 'no_notes'}
    # Join notes into a single string for translation
    text = '\n'.join(notes)
    translated = translate.translate(text, target_language=target_lang)
    return {'status': 'translated', 'translated_text': translated.get('translatedText', '')}
