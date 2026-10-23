import os
import urllib.request
import urllib.error
import json
from typing import Optional

from observability_models import (
    LogQuery,
    LogQueryResponse,
    LogEntry,
    minutes_ago_iso,
    now_iso,
    DATADOG_API_BASE,
    DATADOG_API_KEY,
    DATADOG_APP_KEY,
)


def query_error_logs(
    service: str = "",
    source: str = "",
    severity: str = "error",
    minutes: int = 60,
    limit: int = 100,
    index: str = "main",
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
) -> LogQueryResponse:
    from_time = minutes_ago_iso(minutes)
    to_time = now_iso()
    query_parts = [f"status:{severity}"]
    if service:
        query_parts.append(f"service:{service}")
    if source:
        query_parts.append(f"source:{source}")
    query_str = " ".join(query_parts)
    log_query = LogQuery(
        query=query_str,
        from_time=from_time,
        to_time=to_time,
        index=index,
        limit=limit,
        sort="-timestamp",
    )
    return execute_query(log_query, api_key=api_key, app_key=app_key)


def execute_query(
    log_query: LogQuery,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
) -> LogQueryResponse:
    query_url = f"{DATADOG_API_BASE}/api/v2/logs/events/search"
    params = log_query.to_params()
    query_string = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
    full_url = f"{query_url}?{query_string}"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key or DATADOG_API_KEY,
    }
    if app_key or DATADOG_APP_KEY:
        headers["DD-APPLICATION-KEY"] = app_key or DATADOG_APP_KEY
    req = urllib.request.Request(full_url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_data = resp.read().decode("utf-8")
            if resp_data:
                data = json.loads(resp_data)
                return LogQueryResponse.from_datadog_response(data)
            return LogQueryResponse(status="empty")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(
            f"Datadog log query API error {e.code}: {e.reason} - {error_body}"
        ) from e
