import datetime
from observability_client import ObservabilityClient
from observability_models import LogEntry, LogQueryResult
from google.cloud import logging_v2


def fetch_recent_logs(
    log_name: str, field_filters: dict[str, str], time_range_minutes: int
) -> LogQueryResult:
    client = ObservabilityClient()
    logging_client_v2 = client.get_logging_client()

    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now - datetime.timedelta(minutes=time_range_minutes)

    filter_parts = [f'logName="projects/{client.project_id}/logs/{log_name}']
    for field, value in field_filters.items():
        filter_parts.append(f'{field}="{value}')
    filter_parts.append(f'timestamp>="{start_time.isoformat()}')

    filter_string = " AND ".join(filter_parts)

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
