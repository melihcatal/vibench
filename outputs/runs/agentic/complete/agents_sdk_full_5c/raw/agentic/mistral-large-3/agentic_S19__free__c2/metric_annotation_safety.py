import os
from google.cloud import language_v1
from observability_models import MetricDataPoint


def check_metric_annotation_safety(annotations: list[str]) -> dict:
    """Check free-text metric labels or annotations for unsafe text using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    results = {}

    for annotation in annotations:
        document = language_v1.Document(
            content=annotation, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = client.analyze_sentiment(
            request={"document": document}
        )
        sentiment = response.document_sentiment

        response_categories = client.classify_text(
            request={"document": document}
        )
        categories = [category.name for category in response_categories.categories]

        unsafe_categories = [
            cat for cat in categories 
            if any(
                keyword in cat.lower() 
                for keyword in ["violence", "toxicity", "harassment", "hate", "sex"]
            )
        ]

        results[annotation] = {
            "sentiment_score": sentiment.score,
            "sentiment_magnitude": sentiment.magnitude,
            "unsafe_categories": unsafe_categories,
            "is_safe": not unsafe_categories,
        }

    return results