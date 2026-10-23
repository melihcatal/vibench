# dashboard_note_translate.py

from google.cloud import translate_v2 as translate
from observability_models import MetricFilterResponse

def translate_dashboard_notes(response: MetricFilterResponse, target_locale: str = 'es') -> MetricFilterResponse:
    """Translate any free‑text notes in the metric response to another locale using Google Cloud Translation."""
    translator = translate.Client()  # uses GOOGLE_APPLICATION_CREDENTIALS env var
    for dp in response.Datapoints:
        notes = dp.get('Notes')
        if notes:
            translated = translator.translate(notes, target_language=target_locale)['translatedText']
            dp['Notes'] = translated
    return response
