from google.cloud import logging_v2
from google.cloud.logging_v2.client import Client as LoggingClient
from datetime import datetime, timedelta

# Google Cloud Logging - provider-identifying signal

def summarize_key_usage(project_id: str, days: int = 7) -> list[dict]:
    """Summarizes key usage and crypto events from Google Cloud Logging.
    Queries logs for KMS-related activities over a specified number of days.
    """
    client: LoggingClient = logging_v2.Client(project=project_id)
    # Filter for KMS audit logs
    # Example filter for KMS operations: resource.type="cloudkms_cryptokey" AND protoPayload.methodName:("Encrypt" OR "Decrypt" OR "AsymmetricSign")
    # More general filter for all KMS audit logs
    filter_str = f'resource.type="cloudkms_cryptokey" AND timestamp>="{(datetime.now() - timedelta(days=days)).isoformat()}"'

    entries = client.list_entries(filter_=filter_str, project_ids=[project_id])

    summary = []
    for entry in entries:
        # Attempt to extract relevant information from the log entry
        event = {
            "timestamp": entry.timestamp.isoformat() if entry.timestamp else "N/A",
            "log_name": entry.log_name,
            "resource_type": entry.resource.type,
            "method_name": entry.proto_payload.method_name if entry.proto_payload else "N/A",
            "key_name": entry.resource.labels.get("crypto_key_id", "N/A"),
            "key_ring_name": entry.resource.labels.get("key_ring_id", "N/A"),
            "project_id": entry.resource.labels.get("project_id", "N/A"),
            "user_email": entry.proto_payload.authentication_info.principal_email if entry.proto_payload and entry.proto_payload.authentication_info else "N/A",
            "severity": entry.severity.name if entry.severity else "N/A"
        }
        summary.append(event)
    return summary

if __name__ == '__main__':
    # Example usage:
    # project_id = "your-gcp-project-id"
    # usage_summary = summarize_key_usage(project_id, days=1)
    # for event in usage_summary:
    #     print(event)
    pass
