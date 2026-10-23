from google.cloud import translate_v2 as translate
from fetch_recent_logs import fetch_recent_logs


def translate_log_messages(
    field_filters: dict, target_language: str = "es", hours: int = 1
) -> Dict[str, Any]:
    """
    Translates support-visible log messages to another locale using Google Cloud Translation API.

    Args:
        field_filters: Dictionary of field-value pairs to filter logs.
        target_language: Target language code (e.g., 'es' for Spanish).
        hours: Time range in hours to query logs from.

    Returns:
        Dictionary containing original and translated log messages.
    """
    client = translate.Client()
    logs = fetch_recent_logs(field_filters, hours=hours)

    if not logs:
        return {"summary": "No logs found for the specified filters."}

    results = []
    for log in logs:
        message = log.get("message", "")
        if message:
            translation = client.translate(message, target_language=target_language)
            results.append(
                {
                    "original_message": message,
                    "translated_message": translation["translatedText"],
                }
            )

    return {
        "total_logs_translated": len(results),
        "target_language": target_language,
        "results": results,
    }
