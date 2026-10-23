from security_client import get_logging_client, get_project_id
from security_models import KeyUsageEntry


def get_key_usage_summary() -> list[KeyUsageEntry]:
    """Summarizes GCP KMS key usage from Cloud Audit Logs."""
    client = get_logging_client()
    project_id = get_project_id()

    # Filter for KMS audit logs
    filter_str = (
        'resource.type="cloudkms_cryptokey" '
        'AND log_name="projects/{}/logs/cloudaudit.googleapis.com%2Fdata_access"'.format(
            project_id
        )
    )

    entries = client.list_log_entries(
        resource_names=[f"projects/{project_id}"],
        filter_=filter_str,
        page_size=100,
    )

    summary = []
    for entry in entries:
        summary.append(
            KeyUsageEntry(
                timestamp=str(entry.timestamp),
                principal_email=entry.proto_payload.authentication_info.principal_email,
                method_name=entry.proto_payload.method_name,
                resource_name=entry.proto_payload.resource_name,
            )
        )
    return summary
