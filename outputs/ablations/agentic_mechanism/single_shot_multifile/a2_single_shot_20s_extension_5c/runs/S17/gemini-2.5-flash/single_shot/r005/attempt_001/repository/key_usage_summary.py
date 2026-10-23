from google.cloud import logging_v2
from google.protobuf.json_format import MessageToDict
from security_client import SecurityClients
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse, KeyUsageEvent
from typing import List, Dict, Any

def summarize_key_usage(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    logging_client = SecurityClients.get_logging_client()

    filter_string_parts = [
        f'resource.type="audited_resource"',
        f'resource.labels.service="cloudkms.googleapis.com"',
        f'protoPayload.@type="type.googleapis.com/google.cloud.audit.AuditLog"',
        f'methodName:"google.cloud.kms."'
    ]

    if request.kms_key_id:
        filter_string_parts.append(f'protoPayload.resourceName:"{request.kms_key_id}"')

    if request.start_time:
        filter_string_parts.append(f'timestamp >= "{request.start_time}"')
    if request.end_time:
        filter_string_parts.append(f'timestamp <= "{request.end_time}"')

    filter_string = " AND ".join(filter_string_parts)

    events: List[KeyUsageEvent] = []
    
    for entry in logging_client.list_entries(
        resource_names=[f"projects/{request.project_id}"],
        filter=filter_string,
        page_size=request.page_size,
        page_token=request.page_token,
        order_by="timestamp desc"
    ):
        if entry.proto_payload and entry.proto_payload.type_url == "type.googleapis.com/google.cloud.audit.AuditLog":
            audit_log_dict = MessageToDict(entry.proto_payload, preserving_proto_field_name=True)
            
            method_name = audit_log_dict.get("methodName", "N/A")
            resource_name = audit_log_dict.get("resourceName", "N/A")
            principal_email = audit_log_dict.get("authenticationInfo", {}).get("principalEmail", "N/A")
            
            events.append(KeyUsageEvent(
                timestamp=entry.timestamp.isoformat(),
                method_name=method_name,
                resource_name=resource_name,
                principal_email=principal_email,
                severity=entry.severity.name
            ))
            
    return KeyUsageSummaryResponse(events=events, next_page_token=None)
