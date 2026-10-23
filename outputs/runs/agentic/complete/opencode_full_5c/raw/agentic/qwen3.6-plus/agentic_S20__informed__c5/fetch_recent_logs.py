import os
import json
import sys
from typing import Optional

from observability_models import LogQueryRequest, LogQueryResponse, LogEntry
from observability_client import query_logs, build_time_range, build_field_query


def fetch_recent_logs(
    field_filters: dict[str, str],
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    minutes_ago: int = 30,
    limit: int = 100,
) -> LogQueryResponse:
    request = build_field_query(
        field_filters=field_filters,
        time_from=time_from,
        time_to=time_to,
    )
    if minutes_ago != 30:
        tf, tt = build_time_range(minutes_ago=minutes_ago)
        request.time_from = time_from or tf
        request.time_to = time_to or tt
    request.limit = limit
    request.sort = "-timestamp"
    return query_logs(request)


def format_log_entry(entry: LogEntry) -> dict:
    return {
        "id": entry.id,
        "timestamp": entry.timestamp,
        "severity": entry.severity,
        "service": entry.service,
        "source": entry.source,
        "hostname": entry.hostname,
        "correlation_id": entry.correlation_id,
        "message": entry.message,
        "attributes": entry.raw_attributes,
    }


def main():
    service = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("DD_SERVICE")
    source = sys.argv[2] if len(sys.argv) > 2 else None
    minutes_ago = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else 100

    field_filters = {}
    if service:
        field_filters["service"] = service
    if source:
        field_filters["source"] = source

    response = fetch_recent_logs(
        field_filters=field_filters,
        minutes_ago=minutes_ago,
        limit=limit,
    )

    output = {
        "total": response.total,
        "next_page_token": response.next_page_token,
        "entries": [format_log_entry(e) for e in response.entries],
    }
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
