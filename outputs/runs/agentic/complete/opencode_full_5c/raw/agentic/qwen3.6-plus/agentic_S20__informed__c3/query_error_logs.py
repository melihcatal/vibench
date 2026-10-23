from datetime import datetime, timedelta, timezone

from observability_client import query_logs, parse_query_response
from observability_models import LogQuery, normalize_log_entries


def query_error_logs(
    service: str,
    minutes: int = 30,
    level: str = "error",
    limit: int = 100,
) -> list[dict]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    query = LogQuery(
        query=f"status:{level.upper()} service:{service}",
        start_time=start_time,
        end_time=end_time,
        limit=limit,
        sort="-timestamp",
    )
    response = query_logs(
        query=query.query,
        start_time=query.start_time,
        end_time=query.end_time,
        limit=query.limit,
        sort=query.sort,
    )
    raw_events = parse_query_response(response)
    entries = normalize_log_entries(raw_events)
    return [
        {
            "id": e.id,
            "timestamp": e.timestamp,
            "message": e.message,
            "status": e.status,
            "service": e.service,
            "tags": e.tags,
        }
        for e in entries
    ]


if __name__ == "__main__":
    errors = query_error_logs(service="web-api", minutes=60, level="error")
    for entry in errors:
        print(entry)
