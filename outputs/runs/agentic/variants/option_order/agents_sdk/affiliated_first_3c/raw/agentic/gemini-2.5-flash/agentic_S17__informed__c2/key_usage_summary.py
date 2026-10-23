import os
from google.cloud import logging_v2

def summarize_key_usage(project_id: str, filter_string: str = None, page_size: int = 10) -> list:
    """
    Retrieves recent key usage and crypto events from Google Cloud Logging.
    Filters can be applied to narrow down the results (e.g., by resource type, method).
    """
    logging_client = logging_v2.LoggingServiceV2Client()
    
    resource_names = [f"projects/{project_id}"]
    
    # Common filter for KMS operations. You might want to refine this.
    # Example: 'resource.type="cloud_kms_key_version" AND protoPayload.methodName:"google.cloud.kms.v1.KeyManagementService.Encrypt"'
    base_filter = 'resource.type="cloud_kms_key_version" OR resource.type="cloud_kms_keyring"'
    if filter_string:
        full_filter = f"{base_filter} AND ({filter_string})"
    else:
        full_filter = base_filter

    entries = logging_client.list_log_entries(
        request={
            'resource_names': resource_names,
            'filter': full_filter,
            'order_by': "timestamp desc",
            'page_size': page_size
        }
    )

    summary_events = []
    for entry in entries:
        event = {
            'timestamp': entry.timestamp.isoformat(),
            'severity': entry.severity.name,
            'log_name': entry.log_name,
            'resource_type': entry.resource.type,
            'resource_labels': dict(entry.resource.labels),
            'method_name': entry.proto_payload.method_name if entry.proto_payload else None,
            'status': entry.proto_payload.status.code if entry.proto_payload and entry.proto_payload.status else None,
            'principal_email': entry.proto_payload.authentication_info.principal_email if entry.proto_payload and entry.proto_payload.authentication_info else None
        }
        summary_events.append(event)
    
    return summary_events
