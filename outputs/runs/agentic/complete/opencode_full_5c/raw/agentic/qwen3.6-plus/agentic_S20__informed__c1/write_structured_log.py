import requests
from observability_client import (
    build_datadog_headers,
    build_log_payload,
    get_datadog_logs_api_url,
)
from observability_models import (
    LogWriteRequest,
    LogWriteResponse,
    normalize_log_write_response,
)


def write_structured_log(request: LogWriteRequest) -> LogWriteResponse:
    url = get_datadog_logs_api_url()
    headers = build_datadog_headers()
    payload = build_log_payload(
        service=request.service,
        message=request.message,
        level=request.level,
        attributes=request.attributes,
    )
    if request.hostname:
        payload["hostname"] = request.hostname
    if request.timestamp_ms:
        payload["timestamp"] = request.timestamp_ms

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    return normalize_log_write_response(
        response.status_code, response.json() if response.content else {}
    )
