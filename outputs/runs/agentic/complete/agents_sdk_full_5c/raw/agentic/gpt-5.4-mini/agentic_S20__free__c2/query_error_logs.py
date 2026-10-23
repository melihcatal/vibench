from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import query_entries
from observability_models import LogQueryRequest, entry_to_dict, LogQueryResponse


def main() -> LogQueryResponse:
    now = datetime.now(timezone.utc)
    request = LogQueryRequest(
        severity="ERROR",
        start_time=now - timedelta(hours=1),
        end_time=now,
        fields={"service": "checkout-api"},
        limit=20,
    )
    return LogQueryResponse(entries=[entry_to_dict(e) for e in query_entries(request)])
