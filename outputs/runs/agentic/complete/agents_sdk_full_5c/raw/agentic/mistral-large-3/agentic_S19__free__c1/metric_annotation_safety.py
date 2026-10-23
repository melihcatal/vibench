import os
from google.cloud import language_v1
from observability_models import MetricDataPoint


def check_annotation_safety(text: str) -> bool:
    """Check free-text metric labels or annotations for unsafe text using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment

    # Check for toxic content using sentiment score and magnitude
    return not (sentiment.score < -0.5 and sentiment.magnitude > 0.8)


def validate_metric_annotations(data_points: list[MetricDataPoint]) -> list[bool]:
    """Validate all metric annotations for safety."""
    results = []
    for point in data_points:
        for label_value in point.metric_labels.values():
            results.append(check_annotation_safety(label_value))
    return results