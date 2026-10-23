import os
import re
from typing import Dict, List

from google.cloud import language_v1


def check_unsafe_text(text: str) -> bool:
    """Check for unsafe content in text using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(request={"document": document})
    return response.document_sentiment.magnitude > 0.8 or any(
        category in ["Profanity", "Toxic"]
        for category in client.classify_text(request={"document": document}).categories
    )


def check_metric_annotations(annotations: List[Dict[str, str]]) -> List[Dict]:
    """Check free-text metric labels or annotations for unsafe text."""
    results = []
    for annotation in annotations:
        for key, value in annotation.items():
            if isinstance(value, str) and check_unsafe_text(value):
                results.append(
                    {
                        "key": key,
                        "value": value,
                        "status": "unsafe",
                    }
                )
            else:
                results.append(
                    {
                        "key": key,
                        "value": value,
                        "status": "safe",
                    }
                )
    return results
