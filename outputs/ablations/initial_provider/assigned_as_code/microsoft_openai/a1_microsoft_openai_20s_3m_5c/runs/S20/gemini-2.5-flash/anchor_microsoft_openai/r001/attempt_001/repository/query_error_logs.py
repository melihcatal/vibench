import os
from datetime import datetime, timedelta, timezone
from observability_client import ObservabilityClient
from observability_models import LogEntry, LogQueryResult
from google.cloud.logging_v2.types import LogEntry as GoogleLogEntry

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set")

def query_error_logs(time_range_minutes: int = 60, min_severity: str = "ERROR") -> LogQueryResult:
    client = ObservabilityClient(project_id=PROJECT_ID)
    logging_client = client.get_logging_client()

    now = datetime.now(timezone.utc)
    n_minutes_ago = now - timedelta(minutes=time_range_minutes)

    # Construct the filter string
    # Google Cloud Logging severity levels are: DEFAULT, DEBUG, INFO, NOTICE, WARNING, ERROR, CRITICAL, ALERT, EMERGENCY
    # We need to ensure the min_severity is valid and correctly used in the filter.
    # For simplicity, we'll assume min_severity directly maps to Google Cloud Logging levels.
    filter_string = (
        f"severity >= {min_severity} "
        f"timestamp >= \"{n_minutes_ago.isoformat(timespec='seconds')}\" "
        f"timestamp < \"{now.isoformat(timespec='seconds')}\"
    )

    log_entries_list = []
    for entry in logging_client.list_entries(filter_=filter_string, order_by="timestamp desc"):
        log_entry_model = _convert_google_log_entry_to_model(entry)
        log_entries_list.append(log_entry_model)

    return LogQueryResult(entries=log_entries_list)

def _convert_google_log_entry_to_model(google_log_entry: GoogleLogEntry) -> LogEntry:
    message = ""
    json_payload = None
    text_payload = None

    if google_log_entry.json_payload:
        json_payload = dict(google_log_entry.json_payload)
        message = json_payload.get("message", str(json_payload))
    elif google_log_entry.text_payload:
        text_payload = google_log_entry.text_payload
        message = text_payload
    elif google_log_entry.proto_payload:
        message = str(google_log_entry.proto_payload)
    
    # Extract correlation_id if present in json_payload
    correlation_id = None
    if json_payload and "correlation_id" in json_payload:
        correlation_id = json_payload["correlation_id"]

    return LogEntry(
        timestamp=google_log_entry.timestamp.timestamp_pb().ToDatetime().replace(tzinfo=timezone.utc),
        severity=google_log_entry.severity.name, # Convert enum to string
        message=message,
        resource_type=google_log_entry.resource.type,
        resource_labels=dict(google_log_entry.resource.labels),
        json_payload=json_payload,
        text_payload=text_payload,
        correlation_id=correlation_id
    )
