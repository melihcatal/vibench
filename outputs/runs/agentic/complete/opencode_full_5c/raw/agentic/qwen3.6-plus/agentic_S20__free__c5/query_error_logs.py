import json
from observability_models import (
    LogQueryRequest,
    LogQueryResponse,
    minutes_ago_iso,
    now_iso,
)
from observability_client import query_logs


def query_error_logs(
    service: str = "",
    time_from: str | None = None,
    time_to: str | None = None,
    limit: int = 100,
) -> LogQueryResponse:
    query_parts = [
        "status:error OR status:critical OR status:alert OR status:emergency"
    ]
    if service:
        query_parts.append(f'service:"{service}"')

    request = LogQueryRequest(
        query=" AND ".join(query_parts),
        time_from=time_from or minutes_ago_iso(30),
        time_to=time_to or now_iso(),
        limit=limit,
        sort="-timestamp",
    )
    return query_logs(request)


if __name__ == "__main__":
    response = query_error_logs(service="auth-service", limit=50)
    for entry in response.entries:
        print(
            json.dumps(
                {
                    "id": entry.id,
                    "timestamp": entry.timestamp,
                    "status": entry.status,
                    "message": entry.message,
                    "service": entry.service,
                },
                indent=2,
            )
        )
    print(f"Total error entries: {response.total_count}")
