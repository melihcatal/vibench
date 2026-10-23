import os
from google.cloud import translate_v2 as translate
from observability_models import MetricDataPoint


def translate_text(text: str, target_language: str) -> str:
    """Translate metric or dashboard notes for another locale using Google Cloud Translation API."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']


def translate_metric_annotations(
    data_points: list[MetricDataPoint], 
    target_language: str,
) -> list[MetricDataPoint]:
    """Translate all metric annotations to the target language."""
    translated_points = []
    for point in data_points:
        translated_labels = {
            key: translate_text(value, target_language)
            for key, value in point.metric_labels.items()
        }
        translated_points.append(
            MetricDataPoint(
                timestamp=point.timestamp,
                value=point.value,
                resource_labels=point.resource_labels,
                metric_labels=translated_labels,
            )
        )
    return translated_points