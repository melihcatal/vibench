from datetime import datetime, timezone, timedelta
import requests
from observability_client import (
    build_datadog_headers,
    build_query_payload,
    get_datadog_query_api_url,
)
from observability_models import (
    LogQueryRequest,
    LogQueryResponse,
    normalize_log_query_response,
)


def query_error_logs(
    service: str = None,
    time_from: datetime = None,
    time_to: datetime = None,
    limit: int = 100,
    additional_filters: list = None,
) -> LogQueryResponse:
    filters = ["status:error OR status:crit OR status:emerg OR status:alert"]
    if service:
        filters.append(f"service:{service}")
    if additional_filters:
        filters.extend(additional_filters)

    if time_from is None:
        time_from = datetime.now(timezone.utc) - timedelta(hours=1)
    if time_to is None:
        time_to = datetime.now(timezone.utc)

    time_from_iso = time_from.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    time_to_iso = time_to.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    url = get_datadog_query_api_url()
    headers = build_datadog_headers()
    payload = build_query_payload(
        filters=filters,
        time_from=time_from_iso,
        time_to=time_to_iso,
        limit=limit,
        sort="-timestamp",
    )

    response = requests.post(url, json=payload, headers=headers, timeout=60)
    return normalize_log_query_response(response.json() if response.content else {})
