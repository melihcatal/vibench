from __future__ import annotations

from typing import Any, Dict

from observability_client import query_normalized_logs
from observability_models import LogQueryWindow, summarize_records


def query_error_logs(
    minutes: int = 60, minimum_severity: str = "ERROR"
) -> Dict[str, Any]:
    window = LogQueryWindow.last_minutes(minutes)
    records = query_normalized_logs(window=window, severity=minimum_severity)
    return summarize_records(records)
