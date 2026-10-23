import os
from google.cloud import logging_v2

def summarize_login_audits(project_id: str, filter_string: str = None) -> list:
    client = logging_v2.LoggingServiceV2Client()
    # Project example: 'projects/YOUR_PROJECT_ID'
    project_path = f"projects/{project_id}"
    
    # Example filter: 'resource.type="global" AND protoPayload.methodName="StartFederatedLogin"'
    # Or, to filter by severity: 'severity=ERROR'
    full_filter = 'logName="projects/{}/logs/cloudaudit.googleapis.com%2Factivity" AND protoPayload.serviceName="login.googleapis.com"' \
                  .format(project_id)
    if filter_string:
        full_filter = f"{full_filter} AND ({filter_string})"

    entries = client.list_log_entries(
        resource_names=[project_path],
        filter=full_filter,
        order_by=logging_v2.ListLogEntriesRequest.Order.NEWEST,
        page_size=10 # Limiting to 10 for demonstration
    )

    summary = []
    for entry in entries:
        summary.append({
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity.name,
            "method_name": entry.proto_payload.method_name if entry.proto_payload else "N/A",
            "resource_name": entry.resource.type
        })
    return summary
