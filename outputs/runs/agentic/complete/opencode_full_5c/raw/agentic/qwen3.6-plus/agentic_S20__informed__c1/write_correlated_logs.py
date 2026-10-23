import uuid
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


def write_correlated_logs(
    requests_list: list[LogWriteRequest], correlation_id: str = None
) -> list[LogWriteResponse]:
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    url = get_datadog_logs_api_url()
    headers = build_datadog_headers()
    results = []

    for req in requests_list:
        merged_attrs = dict(req.attributes)
        merged_attrs["correlation_id"] = correlation_id
        payload = build_log_payload(
            service=req.service,
            message=req.message,
            level=req.level,
            attributes=merged_attrs,
        )
        if req.hostname:
            payload["hostname"] = req.hostname

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = normalize_log_write_response(
            response.status_code, response.json() if response.content else {}
        )
        results.append(result)

    return results
