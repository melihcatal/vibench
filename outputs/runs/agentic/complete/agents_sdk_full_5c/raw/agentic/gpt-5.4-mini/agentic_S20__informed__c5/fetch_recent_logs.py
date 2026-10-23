from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import build_client_from_env
from observability_models import LogQuery, ensure_iso8601


def fetch_recent_logs() -> list[dict]:
    client = build_client_from_env()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=30)
    query = LogQuery(
        field_filters={"service": "orders-api", "env": "prod"},
        start_time=ensure_iso8601(start),
        end_time=ensure_iso8601(end),
        limit=50,
    )
    return client.query_logs(query).results
