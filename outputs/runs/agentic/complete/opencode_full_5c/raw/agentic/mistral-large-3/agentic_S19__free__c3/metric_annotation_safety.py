import re
from typing import List, Dict
from google.cloud import language_v1


def check_metric_annotations(annotations: List[str]) -> Dict[str, List[dict]]:
    """Check free-text metric labels or annotations for unsafe text using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    results = {}

    for annotation in annotations:
        document = language_v1.Document(
            content=annotation, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = client.analyze_sentiment(request={"document": document})

        unsafe_content = []
        if response.document_sentiment.magnitude > 0.8:
            unsafe_content.append(
                {
                    "type": "sentiment",
                    "severity": response.document_sentiment.score,
                    "message": "Extreme sentiment detected",
                }
            )

        if re.search(r"\b(password|secret|token|key)\b", annotation, re.IGNORECASE):
            unsafe_content.append(
                {
                    "type": "sensitive_data",
                    "severity": 1.0,
                    "message": "Potential sensitive data detected",
                }
            )

        if unsafe_content:
            results[annotation] = unsafe_content

    return results
