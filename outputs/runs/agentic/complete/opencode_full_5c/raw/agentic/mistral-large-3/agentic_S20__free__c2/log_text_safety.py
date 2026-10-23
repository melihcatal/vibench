from typing import Dict, List
import os

from observability_client import get_logging_client
from google.cloud import language_v1


def check_log_text_safety(log_messages: List[str]) -> List[Dict[str, str]]:
    """
    Checks selected log message text for unsafe content using Google Cloud Natural Language API.

    Args:
        log_messages: A list of log messages to check.

    Returns:
        A list of dictionaries containing the message and its safety analysis results.
    """
    client = language_v1.LanguageServiceClient()
    results = []

    for message in log_messages:
        document = language_v1.Document(
            content=message, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = client.analyze_sentiment(
            request={
                "document": document,
                "encoding_type": language_v1.EncodingType.UTF8,
            }
        )

        # Check for toxic content using sentiment score as a proxy
        is_unsafe = response.document_sentiment.score < -0.5

        results.append(
            {
                "message": message,
                "is_unsafe": is_unsafe,
                "sentiment_score": response.document_sentiment.score,
            }
        )

    return results


def fetch_logs_for_safety_check(
    service: str,
    limit: int = 50,
) -> List[str]:
    """
    Fetches logs from Datadog for safety checking.

    Args:
        service: The service to fetch logs for.
        limit: Maximum number of logs to fetch.

    Returns:
        A list of log messages.
    """
    client = get_logging_client()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)

    query = f"service:{service}"
    results = client.query(
        query=query,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
    )

    return [log.get("message", "") for log in results]


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"
    log_messages = fetch_logs_for_safety_check(service="auth-service", limit=20)
    safety_results = check_log_text_safety(log_messages)
    print("Safety Results:", safety_results)
