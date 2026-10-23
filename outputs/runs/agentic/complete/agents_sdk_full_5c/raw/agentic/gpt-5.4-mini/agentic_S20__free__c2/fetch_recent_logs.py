from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import query_entries
from observability_models import LogQueryRequest, LogQueryResponse, entry_to_dict


def main() -> LogQueryResponse:
    now = datetime.now(timezone.utc)
    request = LogQueryRequest(
        severity="INFO",
        start_time=now - timedelta(minutes=30),
        end_time=now,
        fields={"component": "api"},
        limit=50,
    )
    return LogQueryResponse(entries=[entry_to_dict(e) for e in query_entries(request)])
