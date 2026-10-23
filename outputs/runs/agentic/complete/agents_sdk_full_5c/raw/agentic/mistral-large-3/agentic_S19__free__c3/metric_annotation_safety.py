import os
from google.cloud import language_v1
from observability_models import MetricDataPoint


def check_metric_annotations_safety(data_points: list[MetricDataPoint]) -> dict:
    client = language_v1.LanguageServiceClient()
    
    unsafe_labels = {}
    for point in data_points:
        for label, text in {**point.resource_labels, **point.metric_labels}.items():
            document = language_v1.Document(
                content=text,
                type_=language_v1.Document.Type.PLAIN_TEXT
            )
            response = client.analyze_sentiment(
                request={"document": document}
            )
            
            if response.document_sentiment.score < -0.5:
                unsafe_labels[f"{label}_{point.timestamp}"] = {
                    "text": text,
                    "score": response.document_sentiment.score,
                    "magnitude": response.document_sentiment.magnitude
                }
    
    return {
        "unsafe_count": len(unsafe_labels),
        "unsafe_labels": unsafe_labels
    }