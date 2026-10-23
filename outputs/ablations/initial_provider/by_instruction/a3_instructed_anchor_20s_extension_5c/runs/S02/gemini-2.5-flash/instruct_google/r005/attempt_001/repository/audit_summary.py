from google.cloud import logging

def summarize_audit_events(project_id: str, filter_string: str = ""):
    """
    Summarizes federated-login audit events from Google Cloud Logging.
    """
    logging_client = logging.Client(project=project_id)

    # Example filter: "resource.type=\"global\" AND protoPayload.methodName=\"google.identity.federated.login\""
    entries = logging_client.list_entries(filter_=filter_string, order_by="timestamp desc")

    summary = []
    for entry in entries:
        summary.append({
            "timestamp": entry.timestamp,
            "severity": entry.severity,
            "log_name": entry.log_name,
            "resource_type": entry.resource.type,
            "method_name": entry.proto_payload.method_name if entry.proto_payload else None,
            "status": entry.proto_payload.status.message if entry.proto_payload and entry.proto_payload.status else None
        })
        if len(summary) >= 10: # Limit to 10 entries for a summary
            break

    print("Federated Login Audit Summary (last 10 entries):")
    for item in summary:
        print(f"  Timestamp: {item["timestamp"]}, Severity: {item["severity"]}, Method: {item["method_name"]}, Status: {item["status"]}")

    return summary
