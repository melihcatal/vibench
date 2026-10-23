from google.cloud import logging
from datetime import datetime, timedelta
import os

def query_error_logs(project_id: str, hours_ago: int = 1):
    client = logging.Client(project=project_id)

    now = datetime.utcnow()
    past = now - timedelta(hours=hours_ago)
    filter_string = (
        f'severity >= ERROR '
        f'timestamp >= "{past.isoformat("T")}Z" '
        f'timestamp < "{now.isoformat("T")}Z"'
    )

    print(f"Querying Google Cloud Logging for errors in the last {hours_ago} hour(s)...")
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
        errors = query_error_logs(project_id, hours_ago=2)
        print(f"Found {len(errors)} error logs:")
        for error in errors[:5]: # Print first 5 errors
            print(error)
