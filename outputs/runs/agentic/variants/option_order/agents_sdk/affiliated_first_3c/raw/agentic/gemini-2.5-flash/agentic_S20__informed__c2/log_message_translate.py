from google.cloud import translate_v3 as translate
import os
from typing import List, Dict, Any

# Assuming observability_client and observability_models exist and are in the same directory or importable path
from observability_client import get_project_id, get_logging_v2_client
from observability_models import LogQueryParameters

def translate_log_messages(
    project_id: str,
    log_name: str,
    target_language_code: str = "es", # e.g., 'es' for Spanish, 'fr' for French
    time_range_minutes: int = 60,
    source_language_code: str = "en", # Assuming English as source, auto-detection is also possible
) -> List[Dict[str, Any]]:
    """Translates support-visible log messages for another locale using Google Cloud Translation API.
    Fetches recent logs from a specified log_name and translates their messages.
    """
    client = translate.TranslationServiceClient()

    # The parent resource for the Cloud Translation API is typically the project.
    # Format: projects/PROJECT_ID/locations/global (or specific region)
    parent = f"projects/{project_id}/locations/global"

    logging_client = get_logging_v2_client(project_id)

    # Fetch recent logs from the specified log_name
    query_params = LogQueryParameters(
        project_id=project_id,
        time_range_minutes=time_range_minutes,
        log_name=log_name
    )
    filter_str = query_params.to_gcp_filter_string()

    logs_to_translate = []
    for entry in logging_client.list_entries(order_by=logging_v2.LogEntryOrder.NEWEST, filter_=filter_str, page_size=50): # Limit logs to process
        message = entry.text_payload if entry.text_payload else (entry.json_payload.get("message") if entry.json_payload else None)
        if message:
            logs_to_translate.append({
                "log_id": entry.insert_id,
                "timestamp": str(entry.timestamp),
                "original_message": message,
            })

    if not logs_to_translate:
        print(f"No recent logs found in '{log_name}' for translation.")
        return []

    translated_logs = []
    for log in logs_to_translate:
        text_to_translate = log["original_message"]
        
        try:
            response = client.translate_text(
                request={
                    "parent": parent,
                    "contents": [text_to_translate],
                    "mime_type": "text/plain",  # Mime types: text/plain, text/html
                    "source_language_code": source_language_code,
                    "target_language_code": target_language_code,
                }
            )

            translated_message = ""
            for translation in response.translations:
                translated_message += translation.translated_text

            translated_logs.append({
                "log_id": log["log_id"],
                "timestamp": log["timestamp"],
                "original_message": log["original_message"],
                "translated_message": translated_message,
                "target_language": target_language_code,
            })
        except Exception as e:
            print(f"Error translating log ID {log['log_id']}: {e}")
            translated_logs.append({"log_id": log["log_id"], "original_message": log["original_message"], "error": str(e), "translated_message": None})

    return translated_logs

if __name__ == "__main__":
    project_id = get_project_id()
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
        exit(1)

    log_name_to_translate = "my-app-logs" # Replace with a log name containing messages to translate
    target_locale = "fr" # Translate to French

    print(f"Translating log messages from '{log_name_to_translate}' to '{target_locale}'...")
    translated_results = translate_log_messages(project_id=project_id, log_name=log_name_to_translate, target_language_code=target_locale, time_range_minutes=60)

    if translated_results:
        print(f"\n--- Translated Log Messages ({target_locale}) ---")
        for result in translated_results:
            print(f"Log ID: {result['log_id']}")
            print(f"Original: {result['original_message']}")
            print(f"Translated ({result['target_language']}): {result['translated_message']}")
            print("---")
    else:
        print("No logs were translated or found.")
