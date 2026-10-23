from __future__ import annotations

from typing import Iterable, List

from datadog_api_client.v2.model.content_encoding import ContentEncoding

from observability_client import ensure_required_credentials, get_logs_api, make_http_log, make_http_log_item
from observability_models import StructuredLogEvent


def write_correlated_logs(correlation_id: str, messages: Iterable[str], service: str = "checkout-api") -> dict:
    ensure_required_credentials(require_app_key=False)
    items: List = []
    for index, message in enumerate(messages):
        event = StructuredLogEvent(
            message=message,
            severity="ERROR" if index == 0 else "INFO",
            service=service,
            correlation_id=correlation_id,
            attributes={"workflow": "order-submit", "sequence": index},
        )
        items.append(make_http_log_item(event.to_datadog_log(ddsource="python", ddtags=[f"service:{service}", "scenario:correlated"])))
    response = get_logs_api().submit_log(content_encoding=ContentEncoding.GZIP, body=make_http_log(items))
    return response.to_dict()
