
from google.cloud import logging_v2

def summarize_federated_login_audit_events(project_id: str):
    """Summarizes federated-login audit events from Google Cloud Logging."""

    client = logging_v2.LoggingServiceV2Client()

    # Filter for federated login events.
    # This example filters for "AuthenticationInfo" which typically contains federated identity details.
    # You might need to adjust the filter based on the exact audit log structure for federated logins.
    filter_str = f'resource.type="audited_resource" protoPayload.methodName="google.login.LoginService.FederatedLogin" OR protoPayload.methodName:"google.identity.federation.v1.FederatedLoginService"'

    # You can specify a time range if needed, e.g., 'timestamp>="2023-01-01T00:00:00Z"'
    # For simplicity, this example fetches recent logs.
    entries = client.list_log_entries(
        resource_names=[f"projects/{project_id}"],
        filter=filter_str,
        order_by=logging_v2.ListLogEntriesRequest.Order.NEWEST
    )

    summary = {}
    event_count = 0

    for entry in entries:
        event_count += 1
        # Extract relevant information for summarization
        # This part will highly depend on the actual structure of your audit logs
        # For demonstration, let's try to get some basic info if available.
        if entry.proto_payload and entry.proto_payload.json_payload:
            payload = entry.proto_payload.json_payload
            method_name = payload.get("methodName", "UNKNOWN_METHOD")
            principal_email = payload.get("authenticationInfo", {}).get("principalEmail", "UNKNOWN_USER")

            if principal_email not in summary:
                summary[principal_email] = {}
            if method_name not in summary[principal_email]:
                summary[principal_email][method_name] = 0
            summary[principal_email][method_name] += 1
        else:
            if "UNKNOWN_PAYLOAD" not in summary:
                summary["UNKNOWN_PAYLOAD"] = {"UNKNOWN_METHOD": 0}
            summary["UNKNOWN_PAYLOAD"]["UNKNOWN_METHOD"] += 1


    print(f"Total federated login events found: {event_count}")
    print("Summary by user and event type:")
    for user, events in summary.items():
        print(f"  User: {user}")
        for event_type, count in events.items():
            print(f"    Event Type: {event_type}, Count: {count}")

if __name__ == "__main__":
    # Replace 'YOUR_GCP_PROJECT_ID' with your actual Google Cloud Project ID
    # Ensure you have authenticated to GCP (e.g., gcloud auth application-default login)
    project_id = "YOUR_GCP_PROJECT_ID"
    summarize_federated_login_audit_events(project_id)
