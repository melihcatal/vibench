import os
from google.cloud import logging_v2
from security_client import get_logging_client


def summarize_key_usage(
    project_id: str,
    filter_str: str = 'resource.type="cloudkms_cryptokey" OR resource.type="cloudkms_cryptokeyversion"',
) -> list[dict]:
    client = get_logging_client()
    project_name = f"projects/{project_id}"

    # Google Cloud Logging signal: google.cloud.logging_v2.LoggingServiceV2Client
    # Google Cloud Logging signal: client.list_entries
    entries = client.list_entries(
        request=logging_v2.ListLogEntriesRequest(
            resource_names=[project_name],
            filter=filter_str,
            order_by=logging_v2.ListLogEntriesRequest.OrderBy.NEWEST,
        )
    )

    summaries = []
    for entry in entries:
        summary = {
            "timestamp": entry.timestamp.isoformat(),
            "severity": logging_v2.LogEntry.Severity(entry.severity).name
            if entry.severity
            else "UNKNOWN",
            "log_name": entry.log_name,
            "resource_type": entry.resource.type,
            "resource_labels": dict(entry.resource.labels),
            "operation": "",
            "user_email": "",
        }
        if entry.proto_payload and entry.proto_payload.HasField("audit_log"):
            audit_log = entry.proto_payload.audit_log
            summary["operation"] = audit_log.method_name
            if (
                audit_log.authentication_info
                and audit_log.authentication_info.principal_email
            ):
                summary["user_email"] = audit_log.authentication_info.principal_email

        summaries.append(summary)
    return summaries
