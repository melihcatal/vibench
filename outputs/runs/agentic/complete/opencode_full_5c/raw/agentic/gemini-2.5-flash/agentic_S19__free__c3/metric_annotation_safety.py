import os
from typing import List
from observability_client import ObservabilityClient
from observability_models import Annotation
from google.cloud import language_v1


def metric_annotation_safety(
    project_id: str,
    annotations: List[str],
    sentiment_threshold: float = -0.5,
) -> List[Annotation]:
    client = ObservabilityClient(project_id).get_language_client()

    safety_checks = []
    for text in annotations:
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        sentiment_response = client.analyze_sentiment(document=document)
        sentiment = sentiment_response.document_sentiment

        severity = "UNKNOWN"
        if sentiment.score <= sentiment_threshold:
            severity = (
                "VERY_LIKELY"  # Very negative sentiment might indicate unsafe content
            )
        elif sentiment.score < 0:
            severity = "LIKELY"
        elif sentiment.score == 0:
            severity = "NEUTRAL"
        elif sentiment.score > 0:
            severity = "UNLIKELY"

        safety_checks.append(
            Annotation(
                text=text,
                severity=severity,  # This is a simplified interpretation of safety based on sentiment
            )
        )
    return safety_checks
