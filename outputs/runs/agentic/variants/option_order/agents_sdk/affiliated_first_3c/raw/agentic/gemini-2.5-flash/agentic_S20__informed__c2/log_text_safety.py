import requests
import os
from typing import List, Dict, Any

# Assuming observability_client and observability_models exist and are in the same directory or importable path
from observability_client import get_project_id, get_logging_v2_client
from observability_models import LogQueryParameters

# Perspective API endpoint
PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_log_text_safety(
    project_id: str,
    log_name: str,
    time_range_minutes: int = 60,
    attribute_threshold: float = 0.7,
    api_key: str = None,
) -> List[Dict[str, Any]]:
    """Checks selected log message text for unsafe content using Perspective API.
    Retrieves recent logs from a specified log_name and sends their messages to Perspective API for analysis.
    """
    if api_key is None:
        api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return [{"error": "PERSPECTIVE_API_KEY environment variable not set."}]

    logging_client = get_logging_v2_client(project_id)

    # Fetch recent logs from the specified log_name
    query_params = LogQueryParameters(
        project_id=project_id,
        time_range_minutes=time_range_minutes,
        log_name=log_name
    )
    filter_str = query_params.to_gcp_filter_string()

    recent_logs = []
    for entry in logging_client.list_entries(order_by=logging_v2.LogEntryOrder.NEWEST, filter_=filter_str, page_size=50): # Limit logs to process
        message = entry.text_payload if entry.text_payload else (entry.json_payload.get("message") if entry.json_payload else None)
        if message:
            recent_logs.append({
                "log_id": entry.insert_id,
                "timestamp": str(entry.timestamp),
                "message": message,
            })

    if not recent_logs:
        print(f"No recent logs found in '{log_name}' for safety analysis.")
        return []

    unsafe_logs = []
    for log in recent_logs:
        text_to_analyze = log["message"]
        
        payload = {
            'comment': {'text': text_to_analyze},
            'requestedAttributes': {
                'TOXICITY': {},
                'SEVERE_TOXICITY': {},
                'IDENTITY_ATTACK': {},
                'INSULT': {},
                'PROFANITY': {},
                'THREAT': {},
            },
            'languages': ['en'], # Assuming English logs for now
        }

        try:
            response = requests.post(f"{PERSPECTIVE_API_BASE_URL}?key={api_key}", json=payload)
            response.raise_for_status() # Raise an exception for HTTP errors
            analysis_results = response.json()

            log_is_unsafe = False
            attribute_scores = {}
            for attr, data in analysis_results.get('attributeScores', {}).items():
                score = data.get('summaryScore', {}).get('value')
                if score is not None:
                    attribute_scores[attr] = score
                    if score >= attribute_threshold:
                        log_is_unsafe = True
            
            if log_is_unsafe:
                unsafe_logs.append({
                    "log_id": log["log_id"],
                    "timestamp": log["timestamp"],
                    "message": log["message"],
                    "safety_scores": attribute_scores,
                    "is_unsafe": True
                })

        except requests.exceptions.RequestException as e:
            print(f"Error calling Perspective API for log ID {log['log_id']}: {e}")
            unsafe_logs.append({"log_id": log["log_id"], "message": log["message"], "error": str(e), "is_unsafe": False})

    return unsafe_logs

if __name__ == "__main__":
    project_id = get_project_id()
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
        exit(1)

    log_name_to_check = "my-app-logs" # Replace with a log name that might contain sensitive text
    # Ensure PERSPECTIVE_API_KEY is set in your environment variables.

    print(f"Checking logs in '{log_name_to_check}' for unsafe content...")
    unsafe_results = check_log_text_safety(project_id=project_id, log_name=log_name_to_check, time_range_minutes=120, attribute_threshold=0.8)

    if unsafe_results:
        print("\n--- Unsafe Log Content Detected ---")
        for result in unsafe_results:
            print(f"Log ID: {result['log_id']}")
            print(f"Timestamp: {result['timestamp']}")
            print(f"Message: {result['message']}")
            print(f"Safety Scores: {result['safety_scores']}")
            print("---")
    else:
        print("No unsafe log content detected above the specified threshold.")
