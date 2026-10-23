from typing import Dict, List
import os

from observability_client import get_logging_client
from google.cloud import translate_v2 as translate


def translate_log_messages(
    log_messages: List[str],
    target_language: str = "es",
) -> List[Dict[str, str]]:
    """
    Translates support-visible log messages to another locale using Google Cloud Translation API.

    Args:
        log_messages: A list of log messages to translate.
        target_language: The target language code (e.g., 'es' for Spanish).

    Returns:
        A list of dictionaries containing the original and translated messages.
    """
    translate_client = translate.Client()
    results = []

    for message in log_messages:
        result = translate_client.translate(message, target_language=target_language)
        results.append(
            {
                "original": message,
                "translated": result["translatedText"],
                "detected_language": result["detectedSourceLanguage"],
            }
        )

    return results


def fetch_logs_for_translation(
    service: str,
    limit: int = 50,
) -> List[str]:
    """
    Fetches logs from Datadog for translation.

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
    log_messages = fetch_logs_for_translation(service="support-service", limit=20)
    translated_results = translate_log_messages(log_messages, target_language="fr")
    print("Translated Results:", translated_results)
