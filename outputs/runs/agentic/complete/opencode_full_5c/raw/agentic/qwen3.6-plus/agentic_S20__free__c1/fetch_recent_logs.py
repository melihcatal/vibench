import os
import json
import requests
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any

from observability_client import (
    DATADOG_LOG_QUERY_ENDPOINT,
    DATADOG_API_KEY,
    DATADOG_APP_KEY,
)
from observability_models import (
    LogQueryRequest,
    LogQueryResponse,
    LogEntry,
    normalize_datadog_query_response,
)


def fetch_recent_logs(
    service: Optional[str] = None,
    level: Optional[str] = None,
    hostname: Optional[str] = None,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    limit: int = 50,
    query_filter: Optional[str] = None,
    field_filters: Optional[Dict[str, str]] = None,
) -> LogQueryResponse:
    if time_from is None:
        time_from = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    if time_to is None:
        time_to = datetime.now(timezone.utc).isoformat()

    query_parts = []
    if service:
        query_parts.append(f"service:{service}")
    if level:
        query_parts.append(f"status:{level}")
    if hostname:
        query_parts.append(f"hostname:{hostname}")
    if field_filters:
        for field_name, field_value in field_filters.items():
            query_parts.append(f"@{field_name}:{field_value}")
    if query_filter:
        query_parts.append(query_filter)

    full_query = " AND ".join(query_parts) if query_parts else "*"

    request = LogQueryRequest(
        query=full_query,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
        sort="-timestamp",
    )

    headers = {
        "DD-API-KEY": DATADOG_API_KEY,
        "DD-APPLICATION-KEY": DATADOG_APP_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(
        DATADOG_LOG_QUERY_ENDPOINT,
        headers=headers,
        data=json.dumps(request.to_datadog_payload()),
        timeout=60,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Datadog log query failed with status {response.status_code}: {response.text}"
        )

    raw_response = response.json()
    return normalize_datadog_query_response(raw_response)


def format_log_entries(response: LogQueryResponse) -> List[Dict[str, Any]]:
    formatted = []
    for entry in response.entries:
        formatted.append(
            {
                "id": entry.id,
                "timestamp": entry.timestamp,
                "status": entry.status,
                "service": entry.service,
                "hostname": entry.hostname,
                "message": entry.message,
                "attributes": entry.attributes,
            }
        )
    return formatted


if __name__ == "__main__":
    result = fetch_recent_logs(
        service=os.getenv("DATADOG_SERVICE", "default-service"),
        level="warn",
        limit=30,
        field_filters={"environment": "production"},
    )
    formatted = format_log_entries(result)
    print(
        json.dumps(
            {
                "total_count": result.total_count,
                "entries": formatted,
            },
            indent=2,
        )
    )
