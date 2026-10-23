from __future__ import annotations

from datadog_api_client.v2.model.content_encoding import ContentEncoding

from observability_client import ensure_required_credentials, get_logs_api, make_http_log, make_http_log_item
from observability_models import StructuredLogEvent


def write_structured_log(message: str, severity: str = "INFO", service: str = "checkout-api") -> dict:
    ensure_required_credentials(require_app_key=False)
    event = StructuredLogEvent(
        message=message,
        severity=severity,
        service=service,
        attributes={"component": "payments", "host": "checkout-api-1"},
    )
    body = make_http_log([make_http_log_item(event.to_datadog_log(ddsource="python", ddtags=["team:platform", "env:prod"]))])
    response = get_logs_api().submit_log(content_encoding=ContentEncoding.GZIP, body=body)
    return response.to_dict()
