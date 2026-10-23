from __future__ import annotations

from datetime import datetime
from urllib.parse import quote

from observability_client import build_time_range_filter, get_log_name, get_logging_client, get_project_id, join_filter_parts
from observability_models import LogRecord, normalize_logging_entry


def query_error_logs(start_time: datetime, end_time: datetime, limit: int = 50) -> list[LogRecord]:
    client = get_logging_client()
    project_id = get_project_id()
    log_name = quote(get_log_name(), safe="")
    filter_text = join_filter_parts(
        [
            'severity >= ERROR',
            build_time_range_filter(start_time, end_time),
            f'logName = "projects/{project_id}/logs/{log_name}"',
        ]
    )
    entries = client.list_entries(
        resource_names=[f"projects/{project_id}"],
        filter_=filter_text,
        page_size=limit,
        order_by="timestamp desc",
    )
    return [normalize_logging_entry(entry.to_api_repr()) for entry in entries]
