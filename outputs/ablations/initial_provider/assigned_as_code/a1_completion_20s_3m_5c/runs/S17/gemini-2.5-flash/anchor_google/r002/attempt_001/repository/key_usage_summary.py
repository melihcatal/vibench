from google.cloud import logging_v2
from datetime import datetime, timedelta

def summarize_key_usage(project_id: str, days: int = 7) -> dict:
    client = logging_v2.LoggingServiceV2Client()
    resource_names = [f"projects/{project_id}"]

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    # Filter for KMS audit logs (data access and admin activity)
    filter_str = (
        f'resource.type="audited_resource" '
        f'log_name="projects/{project_id}/logs/cloudaudit.googleapis.com%2Fdata_access" OR '
        f'log_name="projects/{project_id}/logs/cloudaudit.googleapis.com%2Factivity" '
        f'protoPayload.serviceName="cloudkms.googleapis.com" '
        f'timestamp>="{start_time.isoformat(timespec="seconds")}Z" '
        f'timestamp<="{end_time.isoformat(timespec="seconds")}Z"'
    )

    entries = client.list_log_entries(
        resource_names=resource_names,
        filter=filter_str,
        order_by="timestamp desc",
    )

    summary = {
        "total_crypto_operations": 0,
        "key_operations": {},
        "users": {},
        "locations": {},
    }

    for entry in entries:
        summary["total_crypto_operations"] += 1
        payload = entry.proto_payload
        if payload and payload.method_name:
            key_name = "unknown"
            if "resource" in entry.resource.labels and "cryptokey_id" in entry.resource.labels:
                 key_name = entry.resource.labels["cryptokey_id"]
            elif "resourceName" in payload and "cryptoKeys" in payload.resourceName:
                # Attempt to parse key name from resourceName if available in payload
                parts = payload.resourceName.split('/')
                if "cryptoKeys" in parts:
                    key_index = parts.index("cryptoKeys")
                    if key_index + 1 < len(parts):
                        key_name = parts[key_index + 1]

            summary["key_operations"].setdefault(key_name, {})
            summary["key_operations"][key_name].setdefault(payload.method_name, 0)
            summary["key_operations"][key_name][payload.method_name] += 1

            if entry.insert_id and entry.insert_id.startswith("projects/") and "principalEmail" in payload.authentication_info:
                user_email = payload.authentication_info.principal_email
                summary["users"].setdefault(user_email, 0)
                summary["users"][user_email] += 1

            location = entry.resource.labels.get("location", "global")
            summary["locations"].setdefault(location, 0)
            summary["locations"][location] += 1

    return summary
