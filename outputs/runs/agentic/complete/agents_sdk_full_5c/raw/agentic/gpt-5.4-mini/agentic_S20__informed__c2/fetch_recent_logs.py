from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import load_client_from_env
from observability_models import QueryRequest


def fetch_recent_logs() -> list[dict]:
    client = load_client_from_env()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=30)
    request = QueryRequest(
        query='service:checkout-api status:500',
        start_time=start.isoformat().replace("+00:00", "Z"),
        end_time=end.isoformat().replace("+00:00", "Z"),
        limit=100,
    )
    response = client.query_logs(request)
    return response.entries
