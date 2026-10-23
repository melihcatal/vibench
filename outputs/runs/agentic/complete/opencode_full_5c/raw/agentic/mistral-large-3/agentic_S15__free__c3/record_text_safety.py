from typing import Any, Dict, List
import os
from google.cloud import language_v1


client = language_v1.LanguageServiceClient()


def check_text_safety(text: str) -> Dict[str, Any]:
    """Checks text for unsafe content using Google Cloud Natural Language API."""
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment

    response = client.moderate_text(request={"document": document})

    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "moderation_categories": [
            {"name": category.name, "confidence": category.confidence}
            for category in response.moderation_categories
        ],
    }


def record_text_safety(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Checks user-generated document fields for unsafe content."""
    results = []

    for record in records:
        record_body = record.get("body", {})
        text_fields = [
            str(v) for v in record_body.values() if isinstance(v, (str, int, float))
        ]
        text_content = " ".join(text_fields)

        safety_result = check_text_safety(text_content)
        results.append({"id": record["id"], "safety_check": safety_result})

    return results
