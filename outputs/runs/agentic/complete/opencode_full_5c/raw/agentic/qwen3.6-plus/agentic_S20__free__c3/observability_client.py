import json
import os
import urllib.request
import urllib.error
from typing import Any, Optional

from observability_models import (
    LogEvent,
    LogQuery,
    LogQueryResponse,
    LogWriteResponse,
    DATADOG_API_HOST,
    DATADOG_API_BASE,
    DATADOG_LOGS_INTAKE_URL,
    DATADOG_API_KEY,
    DATADOG_APP_KEY,
)


def _build_headers(include_app_key: bool = False) -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": DATADOG_API_KEY,
    }
    if include_app_key and DATADOG_APP_KEY:
        headers["DD-APPLICATION-KEY"] = DATADOG_APP_KEY
    return headers


def _make_request(
    url: str,
    method: str = "GET",
    body: Optional[dict[str, Any]] = None,
    include_app_key: bool = False,
    timeout: int = 30,
) -> dict[str, Any]:
    headers = _build_headers(include_app_key=include_app_key)
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp_data = resp.read().decode("utf-8")
            if resp_data:
                return json.loads(resp_data)
            return {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(
            f"Datadog API error {e.code}: {e.reason} - {error_body}"
        ) from e


def write_log_events(
    events: list[LogEvent],
    api_key: Optional[str] = None,
    dd_source: str = "python-sdk",
) -> LogWriteResponse:
    intake_url = f"{DATADOG_LOGS_INTAKE_URL}/api/v2/logs"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key or DATADOG_API_KEY,
    }
    if dd_source:
        headers["DD-SOURCE"] = dd_source
    payload = {
        "ddsource": dd_source,
        "ddtags": f"env:{os.environ.get('DD_ENV', 'production')}",
        "hostname": os.environ.get("DD_HOSTNAME", ""),
        "service": os.environ.get("DD_SERVICE", ""),
        "logs": [e.to_dict() for e in events],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(intake_url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return LogWriteResponse(
                success=resp.status in (200, 202, 204),
                status_code=resp.status,
                message="Log events submitted to Datadog Logs Intake API",
            )
    except urllib.error.HTTPError as e:
        return LogWriteResponse(
            success=False,
            status_code=e.code,
            message=f"Datadog log ingestion failed: {e.reason}",
        )


def query_logs(log_query: LogQuery) -> LogQueryResponse:
    query_url = f"{DATADOG_API_BASE}/api/v2/logs/events/search"
    params = log_query.to_params()
    query_string = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
    full_url = f"{query_url}?{query_string}"
    response_data = _make_request(full_url, include_app_key=True)
    return LogQueryResponse.from_datadog_response(response_data)


def get_log_config() -> dict[str, str]:
    return {
        "provider": "datadog",
        "api_host": DATADOG_API_HOST,
        "logs_intake_host": f"http-intake.logs.{DATADOG_API_HOST}",
        "api_base": DATADOG_API_BASE,
        "api_key_configured": bool(DATADOG_API_KEY),
        "app_key_configured": bool(DATADOG_APP_KEY),
        "default_index": "main",
    }
