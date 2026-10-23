from observability_client import get_logging_client
from observability_models import build_log_filter
from datetime import datetime, timedelta

def fetch_recent_logs(project_id, time_range_minutes=30, field_filters=None):
    """
    Retrieves recent log results filtered by field values and time range from Google Cloud Logging.
    field_filters example: {"jsonPayload.user_id": "123", "severity": "INFO"}
    """
    client = get_logging_client()

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=time_range_minutes)

    # Separate severity from json_field_filters for build_log_filter
    severity_filter = None
    json_payload_filters = None
    other_filters = {}

    if field_filters:
        field_filters_copy = field_filters.copy()
        severity_filter = field_filters_copy.pop("severity", None)
        json_payload_filters = {k.replace("jsonPayload.", ""): v for k, v in field_filters_copy.items() if k.startswith("jsonPayload.")}
        other_filters = {k: v for k, v in field_filters_copy.items() if not k.startswith("jsonPayload.")}


    filters = build_log_filter(
        severity=severity_filter,
        timestamp_start=start_time.isoformat("T") + "Z",
        timestamp_end=now.isoformat("T") + "Z",
        json_field_filters=json_payload_filters
    )

    # Add other filters if any (e.g., resource.type, logName, etc.)
    if other_filters:
        for key, value in other_filters.items():
            filters += f" {key}=\"{value}\"


    entries = client.list_entries(filter_=filters)

    results = []
    for entry in entries:
        results.append({
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity,
            "resource_type": entry.resource.type,
            "log_name": entry.log_name,
            "payload": entry.payload,
            "labels": entry.labels
        })
    return results

if __name__ == "__main__":
    # Example usage:
    # project_id = "your-gcp-project-id" # Replace with your GCP project ID
    # recent_logs = fetch_recent_logs(project_id, time_range_minutes=5, field_filters={"jsonPayload.user_id": "test_user_456", "severity": "WARNING"})
    # for log in recent_logs:
    #     print(log)
    pass