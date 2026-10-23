import os
import uuid
from datetime import datetime, timezone
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log_item import HTTPLogItem
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from observability_models import CorrelatedLogEvent, CorrelatedLogWriteResponse
from observability_client import get_datadog_config, build_correlated_log_payload


def write_correlated_logs(
    events: list[CorrelatedLogEvent],
    correlation_id: str | None = None,
    service: str = "default-service",
) -> CorrelatedLogWriteResponse:
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        raise ValueError("DD_API_KEY and DD_APP_KEY environment variables are required")

    correlation_id = correlation_id or str(uuid.uuid4())
    config = get_datadog_config(api_key, app_key)

    http_log_items = []
    written_events = []

    for event in events:
        payload = build_correlated_log_payload(event, correlation_id, service)
        http_log_item = HTTPLogItem(
            message=payload["message"],
            ddtags=payload.get("ddtags", ""),
            hostname=payload.get("hostname", ""),
            service=payload.get("service", ""),
            source=payload.get("source", ""),
        )
        http_log_items.append(http_log_item)
        written_events.append(
            {
                "event_id": event.event_id,
                "timestamp": event.timestamp.isoformat(),
                "level": event.level,
            }
        )

    with ApiClient(configuration=config) as api_client:
        logs_api = LogsApi(api_client)
        response = logs_api.submit_log(
            body=http_log_items,
            content_encoding=ContentEncoding.DEFLATE,
        )

    return CorrelatedLogWriteResponse(
        status="accepted" if response is not None else "failed",
        correlation_id=correlation_id,
        events_written=len(written_events),
        events=written_events,
        service=service,
    )


if __name__ == "__main__":
    correlation_id = str(uuid.uuid4())
    events = [
        CorrelatedLogEvent(
            message="Incoming HTTP request received",
            level="info",
            source="api-gateway",
            custom_attributes={"method": "POST", "path": "/api/checkout"},
        ),
        CorrelatedLogEvent(
            message="Payment processing initiated",
            level="info",
            source="payment-service",
            custom_attributes={"amount": 4999, "currency": "USD"},
        ),
        CorrelatedLogEvent(
            message="Payment gateway timeout after 30s",
            level="error",
            source="payment-service",
            custom_attributes={"timeout_ms": 30000, "retry_count": 2},
        ),
    ]
    result = write_correlated_logs(
        events, correlation_id=correlation_id, service="checkout-flow"
    )
    print(result.model_dump_json(indent=2))
