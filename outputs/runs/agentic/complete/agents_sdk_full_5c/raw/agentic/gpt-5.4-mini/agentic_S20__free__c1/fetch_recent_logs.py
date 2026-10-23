from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import query_logs
from observability_models import LogQuery


def main() -> dict:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=30)
    query = LogQuery(
        query='service:payments-api @customer_tier:gold',
        start_time=start_time,
        end_time=end_time,
        limit=25,
    )
    return query_logs(query)
