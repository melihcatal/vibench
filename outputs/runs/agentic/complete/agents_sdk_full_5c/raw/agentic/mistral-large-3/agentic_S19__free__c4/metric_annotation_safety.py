import os
from google.cloud import language_v1
from observability_models import MetricDataPoint


def check_text_safety(text: str) -> bool:
    """Check if text contains unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.moderate_text(document=document)
    return not any(
        category.confidence > 0.7
        for category in response.moderation_categories
    )


def metric_annotation_safety(metric_data: list[MetricDataPoint]) -> dict:
    """Check free-text metric labels or annotations for unsafe text."""
    unsafe_entries = []

    for entry in metric_data:
        for label, value in entry.labels.items():
            if not check_text_safety(value):
                unsafe_entries.append({
                    "timestamp": entry.timestamp,
                    "label": label,
                    "value": value,
                })

    return {
        "is_safe": len(unsafe_entries) == 0,
        "unsafe_entries": unsafe_entries,
    }