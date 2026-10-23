from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import filter_result_rows, query_logs
from observability_models import LogQueryRequest


def fetch_recent_logs(field_values: dict, hours: int = 6) -> dict:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    request = LogQueryRequest(start_time=start, end_time=end, query="")
    result = query_logs(request)
    tables = result.get("tables", [])
    rows = []
    for table in tables:
        rows.extend(table.get("rows", []))
    return {"rows": filter_result_rows(rows, field_values), "status": result.get("status")}
