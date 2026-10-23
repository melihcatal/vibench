import datetime
import os
from observability_client import get_logging_client
from observability_models import LogQueryParameters, LogEntry, LogQueryResult

def fetch_recent_logs(params: LogQueryParameters) -> LogQueryResult:
    logging_client = get_logging_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")

    base_filter = params.filter_string if params.filter_string else ""

    if params.start_time:
        if base_filter:
            base_filter += " AND"
        base_filter += f' timestamp >= "{params.start_time.isoformat(timespec="microseconds")}Z"'
    if params.end_time:
        if base_filter:
            base_filter += " AND"
        base_filter += f' timestamp <= "{params.end_time.isoformat(timespec="microseconds")}Z"'

    entries_list = []
    project_resource = f"projects/{project_id}"

    for entry_payload in logging_client.list_entries(
        resource_names=[project_resource],
        filter_=base_filter.strip(),
        order_by="timestamp desc",
        page_size=params.limit
    ):
        text_payload = getattr(entry_payload, 'text_payload', None)
        json_payload = getattr(entry_payload, 'json_payload', None)
        
        timestamp_dt = None
        if entry_payload.timestamp:
            timestamp_dt = entry_payload.timestamp.ToDatetime().replace(tzinfo=datetime.timezone.utc)

        entries_list.append(
            LogEntry(
                text_payload=text_payload,
                json_payload=dict(json_payload) if json_payload else None,
                severity=entry_payload.severity.name if entry_payload.severity else "UNKNOWN",
                timestamp=timestamp_dt,
                labels=dict(entry_payload.labels) if entry_payload.labels else {},
                log_name=entry_payload.log_name
            )
        )
        if len(entries_list) >= params.limit:
            break

    return LogQueryResult(entries=entries_list)
