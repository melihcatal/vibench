import json
from observability_models import LogQueryResponse, minutes_ago_iso, now_iso
from observability_client import fetch_logs_with_field_filter


def fetch_recent_logs(
    field_name: str,
    field_value: str,
    time_from: str | None = None,
    time_to: str | None = None,
    limit: int = 100,
    extra_query: str = "",
) -> LogQueryResponse:
    return fetch_logs_with_field_filter(
        field_name=field_name,
        field_value=field_value,
        time_from=time_from or minutes_ago_iso(15),
        time_to=time_to or now_iso(),
        limit=limit,
        extra_query=extra_query,
    )


if __name__ == "__main__":
    response = fetch_recent_logs(
        field_name="service",
        field_value="payment-service",
        limit=50,
        extra_query="status:info",
    )
    for entry in response.entries:
        print(
            json.dumps(
                {
                    "id": entry.id,
                    "timestamp": entry.timestamp,
                    "status": entry.status,
                    "message": entry.message,
                    "service": entry.service,
                    "hostname": entry.hostname,
                },
                indent=2,
            )
        )
    print(f"Total entries: {response.total_count}")
