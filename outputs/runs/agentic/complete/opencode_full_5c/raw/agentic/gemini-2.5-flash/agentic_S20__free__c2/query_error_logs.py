import datetime
from observability_client import ObservabilityClient
from observability_models import LogEntry, LogQueryResult
from google.cloud import logging_v2


def query_error_logs(severity: str, time_range_minutes: int) -> LogQueryResult:
    client = ObservabilityClient()
    logging_client_v2 = client.get_logging_client()

    now = datetime.datetime.now(datetime.timezone.utc)
    # Calculate the start time for the query
    start_time = now - datetime.timedelta(minutes=time_range_minutes)

    # Construct the filter string
    # GCP Logging uses `timestamp` for filtering, and `severity` for log level.
    filter_string = f'severity>="{severity}" AND timestamp>="{start_time.isoformat()}"'

    entries = []
    for entry in logging_client_v2.list_entries(
        filter_=filter_string,
        order_by=logging_v2.types.ListLogEntriesRequest.OrderBy.NEWEST,
    ):
        message = entry.text_payload or entry.json_payload or str(entry.proto_payload)
        severity = entry.severity.name
        timestamp = entry.timestamp.isoformat()
        entries.append(
            LogEntry(
                message=message,
                severity=severity,
                timestamp=datetime.datetime.fromisoformat(
                    timestamp.replace("Z", "+00:00")
                ),
            )
        )

    return LogQueryResult(entries=entries)
