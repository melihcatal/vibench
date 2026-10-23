from datetime import datetime, timedelta, timezone

from observability_client import query_logs, parse_query_response
from observability_models import LogQuery, normalize_log_entries


def fetch_recent_logs(
    service: str,
    minutes: int = 15,
    field_filters: dict | None = None,
    limit: int = 50,
) -> list[dict]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    parts = [f"service:{service}"]
    if field_filters:
        for key, value in field_filters.items():
            parts.append(f"{key}:{value}")
    query_str = " AND ".join(parts)
    query = LogQuery(
        query=query_str,
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
            "attributes": e.attributes,
        }
        for e in entries
    ]


if __name__ == "__main__":
    logs = fetch_recent_logs(
        service="web-api",
        minutes=30,
        field_filters={"source": "python"},
        limit=25,
    )
    for entry in logs:
        print(entry)
