from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import build_client_from_env
from observability_models import LogQuery, ensure_iso8601


def query_error_logs() -> list[dict]:
    client = build_client_from_env()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=60)
    query = LogQuery(
        severity="error",
        field_filters={"service": "checkout-api"},
        start_time=ensure_iso8601(start),
        end_time=ensure_iso8601(end),
        limit=25,
    )
    return client.query_logs(query).results
