from datetime import datetime, timezone, timedelta

from observability_models import LogQueryRequest, LogQueryResponse
from observability_client import query_logs, get_default_time_range


def query_error_logs(
    service: str = "",
    source: str = "",
    from_ts: datetime | None = None,
    to_ts: datetime | None = None,
    hours: int = 1,
    limit: int = 100,
) -> LogQueryResponse:
    if from_ts is None or to_ts is None:
        from_ts, to_ts = get_default_time_range(hours=hours)

    query_parts = ["status:error OR status:crit OR status:emergency OR status:alert"]
    if service:
        query_parts.append(f"service:{service}")
    if source:
        query_parts.append(f"source:{source}")

    query = " AND ".join(query_parts)

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
    result = query_error_logs(
        service="payment-service",
        hours=2,
        limit=50,
    )
    for entry in result.entries:
        print(f"[{entry.timestamp}] {entry.status}: {entry.message}")
    print(f"Total: {result.total_count}")
