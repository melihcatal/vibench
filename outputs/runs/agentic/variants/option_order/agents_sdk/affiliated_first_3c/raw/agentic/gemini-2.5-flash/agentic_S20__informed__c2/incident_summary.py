import google.generativeai as genai
import os
from typing import List, Dict, Any

# Assuming observability_client and observability_models exist and are in the same directory or importable path
from observability_client import get_project_id, get_logging_v2_client
from observability_models import LogQueryParameters

def summarize_error_logs(
    project_id: str,
    time_range_minutes: int = 60,
    model_name: str = "gemini-pro", # Using a concrete model identifier
) -> str:
    """Summarizes recent error log entries for incident review using the Google Gemini API."""
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return "Error: GOOGLE_API_KEY environment variable not set. Cannot access Gemini API."
    
    logging_client = get_logging_v2_client(project_id)

    # Use LogQueryParameters to construct the filter for error logs
    query_params = LogQueryParameters(
        project_id=project_id,
        time_range_minutes=time_range_minutes,
        severity="ERROR", # Target ERROR, CRITICAL, ALERT, EMERGENCY
    )
    # The to_gcp_filter_string method of LogQueryParameters only filters for 'ERROR', but Cloud Logging queries can handle `severity >= ERROR` or `severity=(...)`
    # For this summary, we specifically want high severity. Let's modify the filter string directly for more precision.
    # Using the same logic as query_error_logs.py for filter string
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=time_range_minutes)
    start_time_str = start_time.isoformat(timespec='nanoseconds').replace('+00:00', 'Z')
    end_time_str = now.isoformat(timespec='nanoseconds').replace('+00:00', 'Z')
    filter_str = f'severity=("ERROR" OR "CRITICAL" OR "ALERT" OR "EMERGENCY") AND timestamp >= "{start_time_str}" AND timestamp <= "{end_time_str}"'

    error_logs = []
    for entry in logging_client.list_entries(order_by=logging_v2.LogEntryOrder.NEWEST, filter_=filter_str, page_size=100): # Limit logs to process
        log_entry_summary = {
            "timestamp": str(entry.timestamp),
            "severity": entry.severity,
            "log_name": entry.log_name,
            "message": entry.text_payload if entry.text_payload else (entry.json_payload.get("message") if entry.json_payload else str(entry.payload))
        }
        error_logs.append(log_entry_summary)
    
    if not error_logs:
        return f"No error logs found in the last {time_range_minutes} minutes for project {project_id}."

    log_texts = [f"Timestamp: {log['timestamp']}\nSeverity: {log['severity']}\nLog Name: {log['log_name']}\nMessage: {log['message']}" for log in error_logs]
    
    # Prepare the prompt for Gemini
    prompt = f"""Analyze the following error logs and provide a concise incident summary.
    Highlight key issues, potential root causes, frequency, and any notable patterns.
    Focus on actionable insights for an incident response team.

    Error Logs (recent {len(log_texts)} entries):
    {'\n---\n'.join(log_texts)}
    """

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

if __name__ == "__main__":
    project_id = get_project_id()
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
        exit(1)

    print("Fetching and summarizing error logs...")
    summary = summarize_error_logs(project_id=project_id, time_range_minutes=120)
    print("\n--- Incident Summary ---")
    print(summary)
