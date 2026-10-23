import os
from typing import List, Dict
from google.cloud import language_v1
from fetch_recent_logs import fetch_recent_logs


def check_log_text_safety(
    service_name: str, hours_back: int = 1
) -> List[Dict[str, Any]]:
    """
    Checks selected log message text for unsafe content using Google Cloud Natural Language API.

    Args:
        service_name: Name of the service to check logs for
        hours_back: Time range in hours to look back

    Returns:
        List of logs with safety analysis results
    """
    client = language_v1.LanguageServiceClient()

    # Fetch recent logs with messages
    logs = fetch_recent_logs(
        service_name=service_name, field_filters={}, hours_back=hours_back, limit=100
    )

    if not logs:
        return []

    results = []
    for log in logs:
        message = log.get("message", "")
        if not message:
            continue

        document = language_v1.Document(
            content=message, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        response = client.analyze_sentiment(
            request={
                "document": document,
                "encoding_type": language_v1.EncodingType.UTF8,
            }
        )

        # Check for sensitive content using content categories
        response_categories = client.classify_text(request={"document": document})

        sensitive_categories = [
            category.name
            for category in response_categories.categories
            if category.confidence > 0.7
            and any(
                cat in category.name.lower()
                for cat in ["/Adult", "/Health", "/Finance", "/Personal"]
            )
        ]

        results.append(
            {
                "log": log,
                "safety_analysis": {
                    "sentiment_score": response.document_sentiment.score,
                    "sentiment_magnitude": response.document_sentiment.magnitude,
                    "sensitive_categories": sensitive_categories,
                    "is_potentially_unsafe": len(sensitive_categories) > 0
                    or response.document_sentiment.score < -0.7,
                },
            }
        )

    return results
