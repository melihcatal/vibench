from observability_client import ObservabilityClient
from observability_models import QueryFilter, LogEntry
from datetime import datetime, timedelta

def query_error_logs(project_id: str, log_name: str, days_ago: int = 1):
    client = ObservabilityClient(project_id, log_name)

    end_time = datetime.now()
    start_time = end_time - timedelta(days=days_ago)

    query_filter = QueryFilter(
        project_id=project_id,
        log_name=log_name,
        severity="ERROR",
        time_range_start=start_time,
        time_range_end=end_time,
    )

    filter_string = query_filter.to_filter_string()
    log_entries = client.list_log_entries(filter_string)

    # Convert raw log entries to structured LogEntry objects
    structured_entries = []
    for entry in log_entries:
        # Accessing attributes based on google.cloud.logging_v2.entries.LogEntry structure
        structured_entries.append(
            LogEntry(
                log_name=entry.log_name,
                resource_type=entry.resource.type,
                resource_labels=entry.resource.labels,
                timestamp=entry.timestamp,
                severity=entry.severity,
                json_payload=entry.json_payload,
                text_payload=entry.text_payload,
                insert_id=entry.insert_id,
                trace=entry.trace,
                span_id=entry.span_id,
                receive_timestamp=entry.receive_timestamp,
            )
        )

    return structured_entries

