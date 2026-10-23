"""Write a structured JSON log event to Datadog Log Management.

Provider: Datadog HTTP Log Intake API
- Endpoint: POST https://http-intake.logs.datadoghq.com/api/v2/logs
- SDK: datadog-api-client (datadog_api_client.v2.api.logs_api.LogsApi)
- Reference: https://docs.datadoghq.com/api/latest/logs/#send-logs
"""

import os
import sys
import json

from observability_models import StructuredLogEvent
from observability_client import (
    get_observability_client,
    DatadogObservabilityClient,
    DATADOG_LOG_INTAKE_HOST,
)


def write_structured_log(
    message: str,
    service: str,
    status: str = "INFO",
    source: str = "python-app",
    hostname: str | None = None,
    extra: dict | None = None,
    client: DatadogObservabilityClient | None = None,
) -> dict:
    """Write a single structured JSON log event to Datadog Log Management.

    Uses the Datadog HTTP Log Intake API at https://http-intake.logs.datadoghq.com/api/v2/logs
    via the datadog-api-client SDK or direct HTTPS.

    Args:
        message: The human-readable log message.
        service: The service name for log grouping.
        status: Log severity level (INFO, WARN, ERROR, CRITICAL).
        source: The log source identifier.
        hostname: Optional host identifier.
        extra: Additional key-value attributes to attach to the log event.
        client: Optional pre-configured DatadogObservabilityClient.

    Returns:
        Dict with status and response details from Datadog.
    """
    if client is None:
        client = get_observability_client()

    event = StructuredLogEvent(
        message=message,
        service=service,
        status=status,
        source=source,
        hostname=hostname,
        extra_attributes=extra or {},
    )

    payload = event.to_datadog_payload()
    result = client.send_log_events([payload])
    return result


def main():
    """Entry point for writing a structured log event to Datadog."""
    message = os.environ.get("LOG_MESSAGE", "Application started successfully")
    service = os.environ.get("LOG_SERVICE", "web-api")
    status = os.environ.get("LOG_STATUS", "INFO")
    source = os.environ.get("LOG_SOURCE", "python-app")

    result = write_structured_log(
        message=message,
        service=service,
        status=status,
        source=source,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
