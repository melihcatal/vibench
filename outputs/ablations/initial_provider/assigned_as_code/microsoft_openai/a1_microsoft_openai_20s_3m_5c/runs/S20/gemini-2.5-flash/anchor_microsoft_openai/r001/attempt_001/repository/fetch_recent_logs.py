import os
from datetime import datetime, timedelta, timezone
from observability_client import ObservabilityClient
from observability_models import LogEntry, LogQuery, LogQueryResult
from google.cloud.logging_v2.types import LogEntry as GoogleLogEntry

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set")

def fetch_recent_logs(query: LogQuery) -> LogQueryResult:
    client = ObservabilityClient(project_id=PROJECT_ID)
    logging_client = client.get_logging_client()

    # The LogQuery model already has the filter string, so we can use it directly.
    # We also need to add the project_id to the filter if it's not already there implicitly.
    # Google Cloud Logging automatically filters by the project associated with the client.

    log_entries_list = []
    for entry in logging_client.list_entries(filter_=query.filter, order_by=query.order_by, page_size=query.page_size, page_token=query.page_token):
        log_entry_model = _convert_google_log_entry_to_model(entry)
        log_entries_list.append(log_entry_model)

    # Google Cloud Logging's list_entries iterator handles pagination internally.
    # If we need to expose a next_page_token for the LogQueryResult, we'd need to manage it manually
    # or get it from the underlying API call. For simplicity, we'll assume the iterator handles it.
    # If more fine-grained control over pagination is needed, we would use the ._page_iterator attribute
    # or a direct call to the underlying API method `logging_client.logging_service_v2.list_log_entries`.

    # For now, let's assume this returns a complete list for the given query and doesn't directly expose a next_page_token
    # in the same way our model might expect if we were doing manual pagination.
    # If the user provides a page_token, it will be used for the initial fetch.
    # The iterator will fetch subsequent pages transparently up to the page_size limit if it's set.

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

    correlation_id = None
    if json_payload and "correlation_id" in json_payload:
        correlation_id = json_payload["correlation_id"]

    return LogEntry(
        timestamp=google_log_entry.timestamp.timestamp_pb().ToDatetime().replace(tzinfo=timezone.utc),
        severity=google_log_entry.severity.name,
        message=message,
        resource_type=google_log_entry.resource.type,
        resource_labels=dict(google_log_entry.resource.labels),
        json_payload=json_payload,
        text_payload=text_payload,
        correlation_id=correlation_id
    )
