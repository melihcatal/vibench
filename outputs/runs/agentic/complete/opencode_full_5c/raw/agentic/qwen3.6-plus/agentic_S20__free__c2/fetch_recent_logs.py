from datetime import datetime, timezone, timedelta

from observability_models import LogQueryRequest, LogQueryResponse
from observability_client import query_logs, get_default_time_range


def fetch_recent_logs(
    service: str = "",
    status: str = "",
    source: str = "",
    tag: str = "",
    from_ts: datetime | None = None,
    to_ts: datetime | None = None,
    hours: int = 1,
    limit: int = 100,
) -> LogQueryResponse:
    if from_ts is None or to_ts is None:
        from_ts, to_ts = get_default_time_range(hours=hours)

    query_parts = []
    if service:
        query_parts.append(f"service:{service}")
    if status:
        query_parts.append(f"status:{status}")
    if source:
        query_parts.append(f"source:{source}")
    if tag:
        query_parts.append(f"tags:{tag}")

    query = " AND ".join(query_parts) if query_parts else "*"

    request = LogQueryRequest(
        query=query,
        index="main",
        from_ts=from_ts,
        to_ts=to_ts,
        limit=limit,
        sort="-timestamp",
    )
    return query_logs(request)


if __name__ == "__main__":
    result = fetch_recent_logs(
        service="auth-service",
        status="info",
        hours=1,
        limit=25,
    )
    for entry in result.entries:
        print(f"[{entry.timestamp}] {entry.service}: {entry.message}")
    print(f"Total: {result.total_count}")
