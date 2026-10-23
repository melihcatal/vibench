import os
import datetime
from google.cloud import logging_v2
from dotenv import load_dotenv

load_dotenv()

def generate_audit_summary(project_id: str, minutes_ago: int = 60) -> dict:
    """
    Queries Google Cloud Logging for federated login events and generates a summary.

    Args:
        project_id: The Google Cloud project ID.
        minutes_ago: The number of minutes in the past to search for logs.

    Returns:
        A dictionary summarizing the audit events.
    """
    client = logging_v2.LoggingServiceV2Client()

    # Calculate the start time for the log query
    timestamp_from = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_ago)
    timestamp_str = timestamp_from.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Define a filter to find login-related log entries
    # In a real scenario, these logs would be written by the application
    # using structured logging (e.g., jsonPayload.event_type="login_success").
    filter_str = (
        f'resource.type="global" '
        f'AND jsonPayload.event_type:"federated_login" '
        f'AND timestamp >= "{timestamp_str}"'
    )

    # Prepare the request
    request = {
        "resource_names": [f"projects/{project_id}"],
        "filter": filter_str,
        "order_by": "timestamp desc",
        "page_size": 100,
    }

    # Execute the query
    entries = client.list_log_entries(request=request)

    # Process the log entries
    summary = {
        "total_events": 0,
        "successful_logins": 0,
        "failed_logins": 0,
        "providers": set(),
        "users": set(),
    }

    for entry in entries:
        payload = entry.json_payload
        if not payload:
            continue
        
        summary["total_events"] += 1
        summary["providers"].add(payload.get("provider"))
        summary["users"].add(payload.get("user_id"))

        if payload.get("status") == "success":
            summary["successful_logins"] += 1
        elif payload.get("status") == "failure":
            summary["failed_logins"] += 1
    
    summary["providers"] = list(summary["providers"])
    summary["users"] = list(summary["users"])
    
    return summary

# Example of how you might call this function
# if __name__ == '__main__':
#     gcp_project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
#     if gcp_project_id:
#         login_summary = generate_audit_summary(project_id=gcp_project_id, minutes_ago=1440) # 24 hours
#         print(login_summary)
#     else:
#         print("GOOGLE_CLOUD_PROJECT environment variable not set.")
