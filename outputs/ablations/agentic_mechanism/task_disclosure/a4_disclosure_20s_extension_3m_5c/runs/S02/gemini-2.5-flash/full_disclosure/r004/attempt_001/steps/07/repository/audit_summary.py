from google.cloud import logging_v2

def summarize_federated_login_audit_events(project_id: str, filter_string: str = None):
    """
    Summarizes federated-login audit events from Google Cloud Logging.

    Args:
        project_id: The Google Cloud project ID.
        filter_string: Optional filter string to apply to log entries.
                       Example: 'resource.type="audited_resource" protoPayload.methodName="google.iam.admin.v1.CreateServiceAccount"'
    """
    client = logging_v2.Client(project=project_id)

    # Construct the filter for federated login audit events
    # This is a placeholder; a more specific filter might be needed based on actual audit log structure
    base_filter = 'logName:"cloudaudit.googleapis.com" protoPayload.methodName:"google.identity"'
    if filter_string:
        full_filter = f"{base_filter} AND {filter_string}"
    else:
        full_filter = base_filter

    print(f"Fetching logs with filter: {full_filter}")

    log_entries = client.list_entries(
        filter_=full_filter,
        order_by=logging_v2.entries.ListLogEntriesRequest.OrderBy.NEWEST,
        page_size=100  # Fetch up to 100 entries for summarization
    )

    summary = {
        "total_events": 0,
        "event_types": {},
        "users": {},
        "recent_events": []
    }

    for entry in log_entries:
        summary["total_events"] += 1
        method_name = entry.proto_payload.method_name if entry.proto_payload and hasattr(entry.proto_payload, 'method_name') else "UNKNOWN_METHOD"
        summary["event_types"][method_name] = summary["event_types"].get(method_name, 0) + 1

        principal_email = "UNKNOWN_USER"
        if entry.proto_payload and hasattr(entry.proto_payload, 'authentication_info') and entry.proto_payload.authentication_info:
            principal_email = entry.proto_payload.authentication_info.principal_email

        summary["users"][principal_email] = summary["users"].get(principal_email, 0) + 1

        summary["recent_events"].append({
            "timestamp": entry.timestamp.isoformat(),
            "method_name": method_name,
            "principal_email": principal_email,
            "severity": entry.severity.name,
            "log_name": entry.log_name
        })

    # Basic summarization logic (can be expanded)
    print("\n--- Audit Summary ---")
    print(f"Total Federated Login Events: {summary['total_events']}")
    print("\nEvent Types:")
    for event_type, count in summary["event_types"].items():
        print(f"  - {event_type}: {count}")

    print("\nUsers Involved:")
    for user, count in summary["users"].items():
        print(f"  - {user}: {count}")

    print("\nRecent Events (up to 10):")
    for event in summary["recent_events"][:10]:
        print(f"  [{event['timestamp']}] Severity: {event['severity']}, User: {event['principal_email']}, Method: {event['method_name']}")

    return summary

if __name__ == "__main__":
    # Example usage: Replace with your actual Google Cloud Project ID
    # Ensure you have authenticated with Google Cloud (e.g., gcloud auth application-default login)
    # and have the necessary permissions to read logs.
    # project_id = "your-gcp-project-id"
    # summarize_federated_login_audit_events(project_id)
    pass
