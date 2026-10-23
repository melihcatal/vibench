from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import parse_logs_response, query_logs
from observability_models import LogQuery


def main() -> dict:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=6)
    query = LogQuery(
        query='service:checkout-api status:error',
        start_time=start_time,
        end_time=end_time,
        limit=20,
    )
    response = query_logs(query)
    normalized = parse_logs_response({"data": {"results": response.get("payload", [])}})
    return {
        "provider": "datadog",
        "summary": f"Found {normalized['count']} error log candidates for incident review.",
        "results": normalized["results"],
    }
