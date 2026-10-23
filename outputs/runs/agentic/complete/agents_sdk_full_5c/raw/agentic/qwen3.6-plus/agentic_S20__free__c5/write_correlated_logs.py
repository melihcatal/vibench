"""Write application log events with a shared request/correlation identifier to Datadog.

Provider: Datadog HTTP Log Intake API
- Endpoint: POST https://http-intake.logs.datadoghq.com/api/v2/logs
- SDK: datadog-api-client (datadog_api_client.v2.api.logs_api.LogsApi)
- Reference: https://docs.datadoghq.com/tracing/guide/connect_logs_and_traces/
"""

import os
import sys
import json
from typing import Optional

from observability_models import (
    CorrelatedLogEvent,
    generate_correlation_id,
    generate_trace_id,
    generate_span_id,
)
from observability_client import (
    get_observability_client,
    DatadogObservabilityClient,
    DATADOG_LOG_INTAKE_HOST,
)


def write_correlated_logs(
    log_entries: list[dict],
    correlation_id: Optional[str] = None,
    trace_id: Optional[str] = None,
    span_id: Optional[str] = None,
    service: str = "web-api",
    source: str = "python-app",
    hostname: Optional[str] = None,
    request_path: Optional[str] = None,
    request_method: Optional[str] = None,
    client: Optional[DatadogObservabilityClient] = None,
) -> dict:
    """Write multiple log events sharing a correlation/trace ID to Datadog.

    Each log event is enriched with Datadog APM correlation fields
    (dd.trace_id, dd.span_id) and a shared correlation_id for request-level
    log aggregation.

    Reference: https://docs.datadoghq.com/tracing/guide/connect_logs_and_traces/

    Args:
        log_entries: List of dicts with 'message' and optional 'status' keys.
        correlation_id: Shared request correlation ID (generated if None).
        trace_id: Datadog trace ID for APM correlation.
        span_id: Datadog span ID for the current log-emitting operation.
        service: Service name for log grouping.
        source: Log source identifier.
        hostname: Optional host identifier.
        request_path: HTTP request path for context.
        request_method: HTTP request method for context.
        client: Optional pre-configured DatadogObservabilityClient.

    Returns:
        Dict with status and response details from Datadog.
    """
    if client is None:
        client = get_observability_client()

    if correlation_id is None:
        correlation_id = generate_correlation_id()
    if trace_id is None:
        trace_id = generate_trace_id()
    if span_id is None:
        span_id = generate_span_id()

    payloads = []
    for i, entry in enumerate(log_entries):
        event = CorrelatedLogEvent(
            message=entry.get("message", ""),
            service=service,
            status=entry.get("status", "INFO"),
            source=source,
            hostname=hostname,
            correlation_id=correlation_id,
            trace_id=trace_id,
            span_id=span_id,
            request_path=request_path,
            request_method=request_method,
            extra_attributes=entry.get("extra", {}),
        )
        payloads.append(event.to_datadog_payload())

    result = client.send_log_events(payloads)
    result["correlation_id"] = correlation_id
    result["trace_id"] = trace_id
    return result


def main():
    """Entry point for writing correlated log events to Datadog."""
    sample_logs = [
        {"message": "Request received", "status": "INFO", "extra": {"step": "start"}},
        {"message": "Processing payload", "status": "INFO", "extra": {"step": "process"}},
        {"message": "Response sent", "status": "INFO", "extra": {"step": "complete"}},
    ]

    result = write_correlated_logs(
        log_entries=sample_logs,
        service=os.environ.get("LOG_SERVICE", "web-api"),
        request_path="/api/orders",
        request_method="POST",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
