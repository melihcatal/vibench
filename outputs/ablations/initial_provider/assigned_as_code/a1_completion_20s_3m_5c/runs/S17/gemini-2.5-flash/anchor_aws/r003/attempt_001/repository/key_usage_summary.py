from google.cloud import logging_v2

def summarize_key_usage(project_id: str, key_id: str):
    client = logging_v2.LoggingServiceV2Client()
    resource_name = f"projects/{project_id}"
    # Filter for KMS audit logs related to a specific key
    # Note: Timestamp filtering is omitted due to strict import constraints.
    filter_string = (
        f'resource.type="audited_resource" '
        f'resource.labels.service="cloudkms.googleapis.com" '
        f'protoPayload.resourceName:"{key_id}"'
    )

    entries = client.list_log_entries(
        resource_names=[resource_name],
        filter=filter_string,
        order_by=logging_v2.types.ListLogEntriesRequest.OrderBy.TIMESTAMP_DESCENDING
    )

    summary = {"total_events": 0, "event_types": {}}
    for entry in entries:
        summary["total_events"] += 1
        method_name = entry.proto_payload.method_name if entry.proto_payload else "UNKNOWN"
        summary["event_types"][method_name] = summary["event_types"].get(method_name, 0) + 1

    return summary
