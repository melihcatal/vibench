import os
import json
import sys
from typing import Optional

from observability_models import LogQueryRequest, LogQueryResponse, LogEntry
from observability_client import query_logs, build_time_range, build_error_query


def query_error_logs(
    service: Optional[str] = None,
    source: Optional[str] = None,
    correlation_id: Optional[str] = None,
    minutes_ago: int = 30,
    limit: int = 100,
    extra_filters: Optional[str] = None,
) -> LogQueryResponse:
    time_from, time_to = build_time_range(minutes_ago=minutes_ago)
    query = build_error_query(
        service=service,
        source=source,
        correlation_id=correlation_id,
        extra_filters=extra_filters,
    )
    request = LogQueryRequest(
        query=query,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
        sort="-timestamp",
    )
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
    }


def main():
    service = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("DD_SERVICE")
    source = sys.argv[2] if len(sys.argv) > 2 else None
    minutes_ago = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else 100

    response = query_error_logs(
        service=service,
        source=source,
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
