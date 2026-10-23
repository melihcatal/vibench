from google.cloud import logging_v2
from google.cloud.logging_v2.proto import log_entry_pb2
from google.protobuf.json_format import MessageToDict
from typing import Dict, Any, List

from identity_client import GOOGLE_CLOUD_PROJECT_ID

def summarize_login_audit_events(filter_string: str = "resource.type=\"global\" AND log_name=\"projects/{}\"/logs/federated_login_audit AND jsonPayload.event_type=\"login_success\"".format(GOOGLE_CLOUD_PROJECT_ID), limit: int = 10) -> List[Dict[str, Any]]:
    """
    Summarizes federated-login audit events from Google Cloud Logging.

    Args:
        filter_string: A filter expression for logs. Defaults to successful federated logins.
        limit: The maximum number of log entries to retrieve.

    Returns:
        A list of dictionaries, where each dictionary represents a summarized audit event.
    """
    client = logging_v2.client.Client(project=GOOGLE_CLOUD_PROJECT_ID)

    summaries = []
    for entry in client.list_entries(filter_=filter_string, page_size=limit):
        # Convert LogEntry to a dictionary for easier processing
        entry_dict = MessageToDict(entry._pb)

        # Extract relevant fields for a summary
        summary = {
            "timestamp": entry_dict.get("timestamp"),
            "event_type": entry_dict.get("jsonPayload", {}).get("event_type"),
            "user_id": entry_dict.get("jsonPayload", {}).get("user_id"),
            "provider": entry_dict.get("jsonPayload", {}).get("provider"),
            "client_ip": entry_dict.get("jsonPayload", {}).get("client_ip"),
            "severity": entry_dict.get("severity"),
        }
        summaries.append(summary)
        if len(summaries) >= limit:
            break

    return summaries

if __name__ == "__main__":
    print("Fetching latest successful federated login audit summaries...")
    try:
        recent_logins = summarize_login_audit_events(limit=5)
        if recent_logins:
            for i, login in enumerate(recent_logins):
                print(f"\n--- Login Event {i+1} ---")
                for key, value in login.items():
                    print(f"{key}: {value}")
        else:
            print("No recent federated login audit events found.")
    except Exception as e:
        print(f"An error occurred: {e}")
