from __future__ import annotations

from typing import Any, Dict, Optional

from observability_client import query_normalized_logs
from observability_models import LogQueryWindow, summarize_records


def fetch_recent_logs(
    minutes: int = 15,
    field_filters: Optional[Dict[str, str]] = None,
    severity: Optional[str] = None,
) -> Dict[str, Any]:
    window = LogQueryWindow.last_minutes(minutes)
    records = query_normalized_logs(
        window=window, severity=severity, field_filters=field_filters or {}
    )
    return summarize_records(records)
