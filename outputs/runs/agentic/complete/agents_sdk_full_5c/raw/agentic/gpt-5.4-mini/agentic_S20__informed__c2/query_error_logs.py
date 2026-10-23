from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import load_client_from_env
from observability_models import QueryRequest


def query_error_logs() -> list[dict]:
    client = load_client_from_env()
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=2)
    request = QueryRequest(
        query='severity:error service:checkout-api',
        start_time=start.isoformat().replace("+00:00", "Z"),
        end_time=end.isoformat().replace("+00:00", "Z"),
        limit=50,
    )
    response = client.query_logs(request)
    return response.entries
