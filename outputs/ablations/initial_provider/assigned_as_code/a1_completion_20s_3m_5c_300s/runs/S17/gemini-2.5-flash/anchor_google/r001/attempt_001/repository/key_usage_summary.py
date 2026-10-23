import os
from google.cloud import logging_v2
from datetime import datetime, timedelta

# Google Cloud Logging client
# This client will be initialized once for the module to reuse connections.
_logging_client = None

def _get_logging_client():
    global _logging_client
    if _logging_client is None:
        _logging_client = logging_v2.Client(project=os.environ.get("GCP_PROJECT_ID"))
    return _logging_client

def summarize_key_usage(project_id: str, key_id: str, time_window_hours: int = 24):
    client = _get_logging_client()

    # Define the time window for the query
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=time_window_hours)

    # Build a filter for KMS audit logs related to the specific key
    # Using resource.type="global" for KMS keys in global location, adjust if key is regional
    # eventType for KMS is typically "google.cloud.kms.v1.KeyManagementService.*"
    # method for encrypt/decrypt operations would be specific, e.g., Encrypt, Decrypt
    log_filter = (
        f'resource.type="cloudkms_cryptokey" AND '
        f'resource.labels.key_ring_id:"{os.environ.get("GCP_KMS_KEY_RING")}" AND '
        f'resource.labels.crypto_key_id:"{key_id}" AND '
        f'timestamp>="{start_time.isoformat()}" AND '
        f'timestamp<="{end_time.isoformat()}"'
    )

    print(f"Fetching log entries for key {key_id} in project {project_id} for the last {time_window_hours} hours...")
    print(f"Log filter: {log_filter}")

    entries = client.list_entries(filter_=log_filter, project_ids=[project_id])

    usage_summary = {
        "key_id": key_id,
        "total_crypto_operations": 0,
        "operation_types": {},
        "users": {},
        "time_window_start": start_time.isoformat(),
        "time_window_end": end_time.isoformat(),
    }

    for entry in entries:
        usage_summary["total_crypto_operations"] += 1
        method_name = entry.payload.get("methodName") if entry.payload and hasattr(entry.payload, 'get') else "UNKNOWN_METHOD"
        user_email = entry.payload.get("authenticationInfo", {}).get("principalEmail", "UNKNOWN_USER") if entry.payload and hasattr(entry.payload, 'get') else "UNKNOWN_USER"

        usage_summary["operation_types"][method_name] = usage_summary["operation_types"].get(method_name, 0) + 1
        usage_summary["users"][user_email] = usage_summary["users"].get(user_email, 0) + 1

    return usage_summary
