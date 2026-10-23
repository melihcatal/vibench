import os
from google.cloud import logging_v2
from security_models import AuditLogEntry
from typing import List, Dict, Any


def summarize_key_usage(project_id: str, days_back: int = 7) -> List[AuditLogEntry]:
    """
    Summarizes key usage and crypto events by querying Google Cloud Audit Logs.
    Filters for KMS-related audit logs.
    """
    logging_client = logging_v2.Client(project=project_id)

    # Filter for KMS audit logs
    # See https://cloud.google.com/kms/docs/audit-logging
    filter_string = (
        f'resource.type="k8s_cluster" OR resource.type="k8s_pod" OR '  # Generic for now; will refine if specific KMS resource types are available.
        f'logName="projects/{project_id}/logs/cloudaudit.googleapis.com%2Factivity" AND '
        f'protoPayload.serviceName="cloudkms.googleapis.com" AND '
        f'timestamp>="{logging_v2.get_now() - logging_v2.datetime.timedelta(days=days_back)}Z"'
    )

    entries = logging_client.list_entries(
        filter_=filter_string, order_by=logging_v2.DESCENDING
    )

    summary_entries: List[AuditLogEntry] = []
    for entry in entries:
        # Normalize relevant fields from the audit log entry
        proto_payload = entry.proto_payload
        if proto_payload and proto_payload.HasField("audit_log"):
            audit_log = proto_payload.audit_log
            summary_entries.append(
                AuditLogEntry(
                    timestamp=entry.timestamp.isoformat(),
                    resource_name=audit_log.resource_name,
                    method_name=audit_log.method_name,
                    principal_email=audit_log.authentication_info.principal_email,
                    severity=entry.severity,
                    json_payload=entry.json_payload,  # Keep original for full context
                )
            )
    return summary_entries


if __name__ == "__main__":
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        print(f"Summarizing key usage for project {PROJECT_ID} from the last 7 days...")
        usage_summary = summarize_key_usage(PROJECT_ID, days_back=7)
        if usage_summary:
            for entry in usage_summary:
                print(
                    f"Timestamp: {entry.timestamp}, Method: {entry.method_name}, "
                    f"Resource: {entry.resource_name}, Principal: {entry.principal_email}, "
                    f"Severity: {entry.severity}"
                )
        else:
            print("No KMS audit logs found for the specified period.")
