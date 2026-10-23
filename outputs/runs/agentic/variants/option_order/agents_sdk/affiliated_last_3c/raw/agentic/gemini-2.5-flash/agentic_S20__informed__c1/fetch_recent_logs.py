from google.cloud import logging
from datetime import datetime, timedelta
import os

def fetch_recent_logs(project_id: str, field_name: str, field_value: str, hours_ago: int = 1):
    client = logging.Client(project=project_id)

    now = datetime.utcnow()
    past = now - timedelta(hours=hours_ago)
    filter_string = (
        f'{field_name} = "{field_value}" '
        f'timestamp >= "{past.isoformat("T")}Z" '
        f'timestamp < "{now.isoformat("T")}Z"'
    )

    print(f"Fetching recent logs from Google Cloud Logging where {field_name}='{field_value}' in the last {hours_ago} hour(s)...")
    entries = client.list_entries(filter_=filter_string, order_by=logging.DESCENDING)

    results = []
    for entry in entries:
        results.append({
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity,
            "payload": entry.payload,
            "resource": entry.resource.type,
            "log_name": entry.log_name
        })
    return results

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id'.")
    else:
        # Example: Fetch logs related to a specific component or request_id
        recent_logs = fetch_recent_logs(project_id, "jsonPayload.component", "auth-service", hours_ago=1)
        print(f"Found {len(recent_logs)} recent logs:")
        for log in recent_logs[:5]: # Print first 5 logs
            print(log)
