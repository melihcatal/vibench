from google.cloud import logging_v2
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse
from google.cloud.logging_v2.services.logging_service_v2 import LoggingServiceV2Client

def summarize_key_usage(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    """
    Summarizes key usage and crypto events using Google Cloud Logging.
    """
    client: LoggingServiceV2Client = logging_v2.LoggingServiceV2Client()
    
    # Construct the filter for logging.
    # Example filter: "resource.type=kms_cryptokey AND protoPayload.methodName:"google.cloud.kms.v1.KeyManagementService.Encrypt""
    full_filter = f"resource.type=kms_cryptokey AND {request.filter_expression} AND timestamp>="{request.time_range_start}" AND timestamp<="{request.time_range_end}""
    
    usage_events = []
    for entry in client.list_log_entries(
        resource_names=[f"projects/{request.project_id}"],
        filter=full_filter,
        order_by=logging_v2.ListLogEntriesRequest.OrderBy.TIMESTAMP_DESC
    ):
        usage_events.append({
            "timestamp": entry.timestamp.isoformat(),
            "resource_type": entry.resource.type,
            "resource_labels": dict(entry.resource.labels),
            "severity": entry.severity.name,
            "log_name": entry.log_name,
            "proto_payload": dict(entry.proto_payload) if entry.proto_payload else None
        })
    
    return KeyUsageSummaryResponse(usage_events=usage_events)
