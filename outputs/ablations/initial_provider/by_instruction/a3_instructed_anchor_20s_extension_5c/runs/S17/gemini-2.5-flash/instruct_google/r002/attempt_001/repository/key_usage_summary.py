import os
from google.cloud import logging_v2

def summarize_key_usage(project_id: str, key_id: str, days: int = 7) -> list[dict]:
    client = logging_v2.LoggingServiceV2Client()
    resource_names = [f"projects/{project_id}"]

    # Filter for KMS audit logs related to the specific key
    # Adjust the filter as needed for specific operations (e.g., encrypt, decrypt, sign)
    filter_str = (
        f'resource.type="cloudkms_cryptokey" AND '
        f'resource.labels.key_ring_id="{os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING")}" AND '
        f'resource.labels.crypto_key_id="{key_id}" AND '
        f'timestamp>="{os.popen(f'date -v -{days}d "+%Y-%m-%dT%H:%M:%SZ"').read().strip()}"'
    )

    entries = []
    for entry in client.list_log_entries(resource_names=resource_names, filter=filter_str):
        entries.append({
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity.name,
            "log_name": entry.log_name,
            "operation": entry.proto_payload.method_name if entry.proto_payload else "N/A",
            "resource": entry.resource.labels.get("crypto_key_id", "N/A")
        })
    return entries
