import os
from typing import List, Dict
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1") # Or your desired region

def summarize_incident_logs(error_logs: List[Dict]) -> str:
    """Summarizes error-log findings for incident review using Google Cloud Generative AI.

    Args:
        error_logs: A list of error log entries (dictionaries).

    Returns:
        A string containing the summary of the incident.
    """
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    model = GenerativeModel("gemini-pro") # Or another suitable model like "gemini-1.0-pro"

    if not error_logs:
        return "No error logs provided for summarization."

    log_texts = []
    for log in error_logs:
        # Extract relevant parts of the log for summarization
        log_entry_text = f"Severity: {log.get('severity')}, Timestamp: {log.get('timestamp')}"
        if 'jsonPayload' in log and 'message' in log['jsonPayload']:
            log_entry_text += f", Message: {log['jsonPayload']['message']}"
        elif 'textPayload' in log:
            log_entry_text += f", Message: {log['textPayload']}"
        
        # Add other relevant fields if available, e.g., resource, labels
        if 'resource' in log and 'type' in log['resource']:
            log_entry_text += f", Resource Type: {log['resource']['type']}"
        
        log_texts.append(log_entry_text)

    prompt = (
        "Analyze the following error log entries and provide a concise summary suitable for an incident review. "
        "Highlight the main issue, potential root causes, affected components, and suggest immediate actions if discernible. "
        "Do not include any preambles or conversational text, just the summary.\n\n"
        + "\n".join(log_texts)
    )

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (simulated error logs)
    sample_error_logs = [
        {
            "severity": "ERROR",
            "timestamp": "2023-10-27T10:00:00Z",
            "jsonPayload": {"message": "Database connection failed", "service": "backend-api", "error_code": 500},
            "resource": {"type": "gce_instance", "labels": {"instance_id": "123"}}
        },
        {
            "severity": "ERROR",
            "timestamp": "2023-10-27T10:00:15Z",
            "textPayload": "Failed to retrieve user data from cache: Cache service unavailable",
            "resource": {"type": "cloud_run_revision", "labels": {"service_name": "user-service"}}
        },
        {
            "severity": "CRITICAL",
            "timestamp": "2023-10-27T10:01:00Z",
            "jsonPayload": {"message": "High CPU utilization detected on database server", "server_id": "db-prod-01"},
            "resource": {"type": "gce_instance", "labels": {"instance_id": "456"}}
        }
    ]

    incident_summary = summarize_incident_logs(sample_error_logs)
    print("\n--- Incident Summary ---")
    print(incident_summary)
