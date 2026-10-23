"""
[SAME-SCENARIO] write_correlated_logs.py

Writes application log events that include a shared request or correlation identifier
to Datadog Managed Logs. Uses the datadog_api_client SDK targeting the Datadog API.

Correlated logs share a correlation_id and optionally a trace_id / span_id for
distributed tracing correlation within Datadog.
"""

import json
import sys
import uuid
from typing import Dict, Any, List

from datadog_api_client import ApiClient
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem

from observability_client import get_logs_client, build_datadog_log_payload, build_correlation_attributes
from observability_models import StructuredLogEvent


def generate_correlation_id() -> str:
    """Generate a unique correlation identifier for a request context."""
    return str(uuid.uuid4())


def write_correlated_logs(
    correlation_id: str,
    log_events: List[Dict[str, Any]],
    trace_id: str | None = None,
    span_id: str | None = None,
    service: str = "default-service",
    env: str = "production",
) -> Dict[str, Any]:
    """
    Write a batch of correlated log events to Datadog Managed Logs.

    Each log event shares the same correlation_id, enabling grouping
    and traceability across services in Datadog Log Explorer.

    Args:
        correlation_id: Shared request/correlation identifier for all events.
        log_events: List of dicts with keys: message, status, optional attributes.
        trace_id: Optional distributed tracing trace ID (Datadog format).
        span_id: Optional distributed tracing span ID.
        service: Service name for the log events.
        env: Deployment environment.

    Returns:
        Dict with write results and correlation metadata.
    """
    results = []
    http_log_items: List[HTTPLogItem] = []

    for event in log_events:
        message = event.get("message", "")
        status = event.get("status", "info")
        event_attrs = event.get("attributes", {})

        correlation_attrs = build_correlation_attributes(
            correlation_id=correlation_id,
            trace_id=trace_id,
            span_id=span_id,
            request_path=event_attrs.get("http.url"),
        )

        combined_attrs = {**event_attrs, **correlation_attrs}

        log_event = StructuredLogEvent(
            message=message,
            service=service,
            env=env,
            status=status,
            ddsource="python",
            attributes=combined_attrs,
        )
        payload = log_event.to_datadog_payload()
        http_log_items.append(HTTPLogItem(**payload))
        results.append({"message": message, "status": "queued"})

    try:
        logs_api: LogsApi = get_logs_client()
        with ApiClient() as api_client:
            body = HTTPLog(http_log_items)
            logs_api.submit_log(body=body)
        for r in results:
            r["status"] = "success"
        return {
            "status": "success",
            "correlation_id": correlation_id,
            "trace_id": trace_id,
            "events_written": len(results),
            "results": results,
        }
    except Exception as exc:
        return {
            "status": "error",
            "correlation_id": correlation_id,
            "message": f"Failed to write correlated logs to Datadog: {exc}",
        }


def write_request_flow_logs(
    request_path: str,
    service: str = "default-service",
    env: str = "production",
) -> Dict[str, Any]:
    """
    Convenience function to write a standard request flow with correlated logs.

    Writes request_received, processing, and request_completed log events
    all sharing the same correlation_id for end-to-end visibility in Datadog.
    """
    correlation_id = generate_correlation_id()
    trace_id = str(uuid.uuid4()).replace("-", "")[:16]

    log_events = [
        {
            "message": f"Request received: {request_path}",
            "status": "info",
            "attributes": {"http.url": request_path, "http.method": "GET"},
        },
        {
            "message": f"Processing request: {request_path}",
            "status": "info",
            "attributes": {"stage": "processing"},
        },
        {
            "message": f"Request completed: {request_path}",
            "status": "info",
            "attributes": {"stage": "completed"},
        },
    ]

    return write_correlated_logs(
        correlation_id=correlation_id,
        log_events=log_events,
        trace_id=trace_id,
        service=service,
        env=env,
    )


def main() -> None:
    """CLI entry point for writing correlated logs to Datadog."""
    if len(sys.argv) < 2:
        print("Usage: write_correlated_logs.py <request_path> [service] [env]")
        sys.exit(1)

    request_path = sys.argv[1]
    service = sys.argv[2] if len(sys.argv) > 2 else "default-service"
    env = sys.argv[3] if len(sys.argv) > 3 else "production"

    result = write_request_flow_logs(request_path, service, env)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
