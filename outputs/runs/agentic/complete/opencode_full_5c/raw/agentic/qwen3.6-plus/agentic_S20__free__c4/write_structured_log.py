import os
from datetime import datetime, timezone
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log_item import HTTPLogItem
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from observability_models import StructuredLogEvent, LogWriteResponse
from observability_client import get_datadog_config, build_log_payload


def write_structured_log(
    message: str,
    level: str = "info",
    service: str = "default-service",
    source: str = "python-app",
    custom_attributes: dict | None = None,
) -> LogWriteResponse:
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        raise ValueError("DD_API_KEY and DD_APP_KEY environment variables are required")

    config = get_datadog_config(api_key, app_key)
    log_event = StructuredLogEvent(
        message=message,
        level=level,
        service=service,
        source=source,
        timestamp=datetime.now(timezone.utc),
        custom_attributes=custom_attributes or {},
    )

    payload = build_log_payload(log_event)
    http_log_item = HTTPLogItem(
        message=payload["message"],
        ddtags=payload.get("ddtags", ""),
        hostname=payload.get("hostname", ""),
        service=payload.get("service", ""),
        source=payload.get("source", ""),
    )

    with ApiClient(configuration=config) as api_client:
        logs_api = LogsApi(api_client)
        response = logs_api.submit_log(
            body=[http_log_item],
            content_encoding=ContentEncoding.DEFLATE,
        )

    return LogWriteResponse(
        status="accepted" if response is not None else "failed",
        event_id=log_event.event_id,
        timestamp=log_event.timestamp.isoformat(),
        service=service,
    )


if __name__ == "__main__":
    result = write_structured_log(
        message="Application started successfully",
        level="info",
        service="payment-gateway",
        source="main",
        custom_attributes={"version": "2.1.0", "region": "us-east-1"},
    )
    print(result.model_dump_json(indent=2))
