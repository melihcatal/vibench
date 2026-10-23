from typing import List, Dict
from google.cloud import translate_v2 as translate
from fetch_recent_logs import fetch_recent_logs


def translate_log_messages(
    service_name: str,
    target_language: str = "es",
    hours_back: int = 1,
    field_filters: Dict[str, str] = None,
) -> List[Dict[str, str]]:
    """
    Translates support-visible log messages to another locale using Google Cloud Translation API.

    Args:
        service_name: Name of the service to fetch logs from
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        hours_back: Time range in hours to look back
        field_filters: Additional filters for log retrieval

    Returns:
        List of dictionaries with original and translated messages
    """
    if field_filters is None:
        field_filters = {}

    client = translate.Client()

    # Fetch logs with messages
    logs = fetch_recent_logs(
        service_name=service_name,
        field_filters=field_filters,
        hours_back=hours_back,
        limit=50,
    )

    if not logs:
        return []

    results = []
    for log in logs:
        message = log.get("message", "")
        if not message:
            continue

        # Translate the message
        translation = client.translate(
            message, target_language=target_language, format_="text"
        )

        results.append(
            {
                "original_log": log,
                "original_message": message,
                "translated_message": translation["translatedText"],
                "detected_source_language": translation["detectedSourceLanguage"],
            }
        )

    return results
