from security_client import SecurityClient
from security_models import AuditLogEntry


def summarize_key_usage(
    project_id: str, key_id: str, days: int = 7
) -> list[AuditLogEntry]:
    client = SecurityClient()
    # Construct a filter to search for KMS-related audit logs for a specific key
    # This filter is an example and might need adjustment based on actual log formats.
    from datetime import datetime, timedelta
    now = datetime.now()
    time_ago = now - timedelta(days=days)
    filter_string = (
        f'resource.type="audited_resource" '
        f'resource.labels.service="cloudkms.googleapis.com" '
        f'protoPayload.resourceName:"keys/{key_id}" '
        f'timestamp>="{time_ago.isoformat()}"'
    )

    entries = []
    for entry in client.logging_client.list_entries(resource_names=[f"projects/{project_id}"], filter_=filter_string):

    entries = []
    for entry in client.logging_client.list_entries(
        resource_names=[f"projects/{project_id}"], filter_=filter_string
    ):
        payload = entry.proto_payload
        if payload and payload.audit_log:
            audit_log = payload.audit_log
            entries.append(
                AuditLogEntry(
                    timestamp=entry.timestamp.isoformat(),
                    event_type=audit_log.method_name,
                    resource_name=audit_log.resource_name,
                    user_agent=audit_log.authentication_info.principal_email
                    if audit_log.authentication_info
                    else "N/A",
                    metadata=audit_log.metadata,
                )
            )
    return entries
