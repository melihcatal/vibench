from google.cloud import logging_v2
from google.cloud.logging_v2.client import Client
from security_client import get_gcp_project_id
from security_models import KeyUsageEvent
import datetime

def summarize_key_usage(project_id: str, days_ago: int = 7) -> list[KeyUsageEvent]:
    """Summarizes key usage and crypto events from Google Cloud Logging.

    Args:
        project_id: The GCP project ID.
        days_ago: How many days back to look for logs.

    Returns:
        A list of KeyUsageEvent objects.
    """
    client: Client = logging_v2.Client(project=project_id)
    
    # Filter for KMS audit logs related to crypto operations
    # Example: filter for encrypt/decrypt operations. Adjust as needed.
    # More log details here: https://cloud.google.com/kms/docs/audit-logs
    filter_str = f"resource.type=\"cloudkms_cryptokey\" AND protoPayload.methodName=(\"google.cloud.kms.v1.KeyManagementService.Encrypt\" OR \"google.cloud.kms.v1.KeyManagementService.Decrypt\" OR \"google.cloud.kms.v1.KeyManagementService.AsymmetricSign\")"
    
    # Only include logs from the last `days_ago` days
    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(days=days_ago)
    filter_str += f" AND timestamp>=\"{start_time.isoformat('T')}\""

    entries = client.list_entries(filter_=filter_str, project_ids=[project_id])

    summary_events: list[KeyUsageEvent] = []
    for entry in entries:
        method_name = entry.proto_payload.method_name if entry.proto_payload else "N/A"
        key_name = entry.resource.labels.get("crypto_key_id", "N/A") # Assuming crypto_key_id in resource labels
        
        # Attempt to extract full key path from textPayload or other fields if not in resource labels
        if key_name == "N/A" and entry.text_payload and "cryptoKey" in entry.text_payload:
            # This is a very basic attempt; a more robust parser might be needed for varied log formats
            parts = entry.text_payload.split("cryptoKey:")
            if len(parts) > 1:
                key_name = parts[1].split(" ")[0].strip()

        summary_events.append(KeyUsageEvent(
            timestamp=entry.timestamp.isoformat() if entry.timestamp else "N/A",
            key_name=key_name,
            operation=method_name.split('.')[-1] if '.' in method_name else method_name,
            user_agent=entry.proto_payload.request_metadata.caller_supplied_user_agents[0] if entry.proto_payload and entry.proto_payload.request_metadata and entry.proto_payload.request_metadata.caller_supplied_user_agents else "N/A",
            resource_type=entry.resource.type
        ))
    return summary_events

if __name__ == '__main__':
    PROJECT_ID = get_gcp_project_id() # Ensure GOOGLE_CLOUD_PROJECT env var is set
    DAYS_AGO = 7

    try:
        usage_summary = summarize_key_usage(PROJECT_ID, DAYS_AGO)
        print(f"Key Usage Summary for project {PROJECT_ID} over last {DAYS_AGO} days:")
        if usage_summary:
            for event in usage_summary:
                print(f"  Timestamp: {event.timestamp}, Key: {event.key_name}, Operation: {event.operation}, User Agent: {event.user_agent}")
        else:
            print("  No key usage events found.")
    except Exception as e:
        print(f"Error summarizing key usage: {e}")
