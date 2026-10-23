import os
from google.cloud import logging_v2
from typing import List, Dict, Any
from identity_models import AuditRecord

# Google Cloud Logging specific client and project ID
GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "your-gcp-project-id")


def summarize_audit_events(entries_limit: int = 10) -> List[AuditRecord]:
    client = logging_v2.Client(project=GOOGLE_PROJECT_ID)

    # Google Cloud Logging filter to find relevant audit events
    # This is a simplified filter; a real application would have more specific criteria.
    # Example: Look for logs related to 'authentication' or 'login' events.
    # For more complex queries, refer to Google Cloud Logging's advanced filters.
    filter_string = (
        'resource.type="global" '  # Or specify a more relevant resource type
        'logName="projects/{}/logs/federated-login-audit" '
        'jsonPayload.event_type=("login" OR "logout" OR "session_refresh")'
    ).format(GOOGLE_PROJECT_ID)

    audit_summaries: List[AuditRecord] = []
    for entry in client.list_entries(filter_=filter_string, page_size=entries_limit):
        payload = entry.json_payload or {}
        audit_record = AuditRecord(
            timestamp=entry.timestamp.isoformat(),
            event_type=payload.get("event_type", "unknown"),
            user_id=payload.get("user_id", "anonymous"),
            provider=payload.get("provider", "unknown"),
            details=payload.get("details", {}),
        )
        audit_summaries.append(audit_record)

    # Google Cloud Logging SDK import: google.cloud.logging_v2
    return audit_summaries


if __name__ == "__main__":
    # To run this example, ensure GOOGLE_PROJECT_ID is set in your environment
    # and you have authenticated your Google Cloud SDK (e.g., `gcloud auth application-default login`).
    # Also, ensure 'google-cloud-logging' is installed: pip install google-cloud-logging
    try:
        print(
            f"Fetching last 10 federated login audit events from Google Cloud Logging for project {GOOGLE_PROJECT_ID}..."
        )
        summaries = summarize_audit_events(entries_limit=5)
        if summaries:
            for i, record in enumerate(summaries):
                print(f"--- Audit Record {i + 1} ---")
                print(f"Timestamp: {record.timestamp}")
                print(f"Event Type: {record.event_type}")
                print(f"User ID: {record.user_id}")
                print(f"Provider: {record.provider}")
                print(f"Details: {record.details}")
        else:
            print("No audit events found.")
    except Exception as e:
        print(f"Error summarizing audit events: {e}")
        print(
            "Please ensure 'google-cloud-logging' is installed and you are authenticated to Google Cloud."
        )
