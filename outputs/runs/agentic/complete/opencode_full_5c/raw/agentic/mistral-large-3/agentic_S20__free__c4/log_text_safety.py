import os
from google.cloud import language_v1
from fetch_recent_logs import fetch_recent_logs


def check_log_text_safety(field_filters: dict, hours: int = 1) -> Dict[str, Any]:
    """
    Checks selected log message text for unsafe content using Google Cloud Natural Language API.

    Args:
        field_filters: Dictionary of field-value pairs to filter logs.
        hours: Time range in hours to query logs from.

    Returns:
        Dictionary containing safety analysis results for log messages.
    """
    client = language_v1.LanguageServiceClient()
    logs = fetch_recent_logs(field_filters, hours=hours)

    if not logs:
        return {"summary": "No logs found for the specified filters."}

    results = []
    for log in logs:
        message = log.get("message", "")
        document = language_v1.Document(
            content=message, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        response = client.analyze_sentiment(request={"document": document})

        safety_analysis = {
            "message": message,
            "sentiment_score": response.document_sentiment.score,
            "sentiment_magnitude": response.document_sentiment.magnitude,
            "unsafe_content": _is_unsafe(response.document_sentiment),
        }
        results.append(safety_analysis)

    return {
        "total_logs_analyzed": len(logs),
        "unsafe_logs_count": sum(1 for r in results if r["unsafe_content"]),
        "results": results,
    }


def _is_unsafe(sentiment) -> bool:
    """
    Determines if the sentiment indicates unsafe content.

    Args:
        sentiment: Sentiment analysis result from Google Cloud NLP.

    Returns:
        Boolean indicating if the content is unsafe.
    """
    return sentiment.score < -0.5 or sentiment.magnitude > 2.0
