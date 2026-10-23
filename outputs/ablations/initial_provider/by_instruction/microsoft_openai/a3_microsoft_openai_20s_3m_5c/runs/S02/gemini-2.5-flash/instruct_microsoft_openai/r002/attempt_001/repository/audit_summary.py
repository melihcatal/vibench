import os
from google.cloud import logging_v2
from datetime import datetime, timedelta

def summarize_login_audit_events(project_id: str, days: int = 7) -> dict:
    """Summarizes federated-login audit events from Google Cloud Logging for a given period."""
    client = logging_v2.Client(project=project_id)

    # Define the time range for the audit events
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    # Filter for federated login events (adjust filter as needed for specific log entries)
    # This is a generic filter, in a real scenario, you'd refine it based on your log structure.
    log_filter = f"timestamp>=\"{start_time.isoformat()}\" AND timestamp<\"{end_time.isoformat()}\" AND logName=\"projects/{project_id}/logs/cloudaudit.googleapis.com%2Factivity\" AND protoPayload.methodName=\"google.identity.federated.v1.LoginService.FederatedLogin\""
    # A more general filter could be: resource.type="global" AND protoPayload.serviceName="login.googleapis.com"

    print(f"Searching Google Cloud Logging for audit events in project '{project_id}' for the last {days} days...")
    entries = client.list_entries(filter_=log_filter, order_by=logging_v2.ListLogEntriesRequest.OrderBy.NEWEST)

    summary = {
        "total_events": 0,
        "successful_logins": 0,
        "failed_logins": 0,
        "users_impacted": set(),
        "event_details": []
    }

    for entry in entries:
        summary["total_events"] += 1
        # Extract relevant information from log entry
        user = entry.json_payload.get("authenticationInfo", {}).get("principalEmail", "unknown") if entry.json_payload else "unknown"
        status = "success" if entry.json_payload.get("status", {}).get("code", 0) == 0 else "failure" if entry.json_payload else "unknown"
        method = entry.proto_payload.method_name if entry.proto_payload else "unknown"
        timestamp = entry.timestamp.isoformat()

        summary["users_impacted"].add(user)
        if status == "success":
            summary["successful_logins"] += 1
        else:
            summary["failed_logins"] += 1

        summary["event_details"].append({
            "timestamp": timestamp,
            "user": user,
            "method": method,
            "status": status,
            "log_id": entry.insert_id
        })

    summary["users_impacted"] = list(summary["users_impacted"])
    print(f"Found {summary["total_events"]} audit events.")
    return summary

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")

    if GCP_PROJECT_ID == "your-gcp-project-id":
        print("Please set the GCP_PROJECT_ID environment variable or replace the placeholder.")
    else:
        audit_summary = summarize_login_audit_events(GCP_PROJECT_ID, days=30) # Summarize for last 30 days
        print("\n--- Audit Summary ---")
        print(f"Total Events: {audit_summary["total_events"]}")
        print(f"Successful Logins: {audit_summary["successful_logins"]}")
        print(f"Failed Logins: {audit_summary["failed_logins"]}")
        print(f"Unique Users Impacted: {len(audit_summary["users_impacted"])}")
        print("Users:", audit_summary["users_impacted"])
        # print("Event Details:", audit_summary["event_details"])
