from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import build_client
from observability_models import coerce_events


def query_error_logs() -> list:
    client = build_client()
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=6)
    response = client.query_logs(
        query='service:checkout-api status:error OR level:error',
        start=start,
        end=end,
        limit=50,
    )
    return coerce_events(response)
