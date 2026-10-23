from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import build_client
from observability_models import coerce_events


def fetch_recent_logs() -> list:
    client = build_client()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=30)
    response = client.query_logs(
        query='service:checkout-api env:production region:us-east-1',
        start=start,
        end=end,
        limit=100,
    )
    return coerce_events(response)
