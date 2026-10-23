# [LATER-STEP] dashboard_note_translate.py

import os
from google.cloud import translate_v2 as translate
from observability_models import MetricFilterRequest, MetricFilterResponse

TRANSLATE_CLIENT = translate.Client()
TARGET_LOCALE = os.getenv('TARGET_LOCALE', 'es')  # e.g., Spanish


def translate_dashboard_note(note: str) -> str:
    """Translate a metric or dashboard note to another locale using Google Cloud Translation API."""
    result = TRANSLATE_CLIENT.translate(note, target_language=TARGET_LOCALE)
    return result['translatedText']


def translate_notes_from_filter(namespace: str, metric_name: str, start_time: str, end_time: str,
                                resource_label: str, label_value: str) -> List[str]:
    """Fetch metric data with a filter and translate each note found in the response."""
    client = CloudWatchClient()
    request = MetricFilterRequest(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimensions=[{'Name': resource_label, 'Value': label_value}],
        period=60,
        statistics=['Average']
    )
    response = client.get_metric_data(request)
    # Assuming response contains 'notes' field per datapoint (placeholder)
    notes = []
    for dp in response.get('datapoints', []):
        note = dp.get('note', '')
        translated = translate_dashboard_note(note)
        notes.append(translated)
    return notes
