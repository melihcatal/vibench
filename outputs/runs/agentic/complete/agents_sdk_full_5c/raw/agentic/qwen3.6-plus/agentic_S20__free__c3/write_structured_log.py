"""
[SAME-SCENARIO] Writes a structured JSON log event to Datadog managed logging service.

Uses the Datadog HTTP Log Intake API v2 (https://http-intake.logs.datadoghq.com/api/v2/logs)
to send a single structured log entry. Requires DD_API_KEY environment variable.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from observability_models import LogEvent, format_time_window
from observability_client import send_logs_to_datadog


def write_structured_log(
    message: str,
    status: str = "info",
    service: str = "web-app",
    hostname: str = "prod-server-01",
    custom_attributes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Write a single structured JSON log event to Datadog.

    Args:
        message: The log message text.
        status: Severity level (info, warn, error, debug, critical).
        service: Service name for grouping logs.
        hostname: Host identifier.
        custom_attributes: Additional key-value pairs to include in the log.

    Returns:
        Response metadata including status code and success indicator.
    """
    event = LogEvent(
        message=message,
        status=status,
        service=service,
        hostname=hostname,
        custom_attributes=custom_attributes or {},
    )

    payload = event.to_payload()
    result = send_logs_to_datadog([payload])
    return result


def main() -> None:
    """Example: write a structured log event to Datadog."""
    result = write_structured_log(
        message="Application health check completed successfully",
        status="info",
        service="api-gateway",
        hostname="prod-server-01",
        custom_attributes={
            "http.method": "GET",
            "http.url": "/health",
            "http.status_code": 200,
            "duration_ms": 12.4,
        },
    )
    print(json.dumps(result, indent=2))
    if not result.get("ok"):
        print(f"Failed to write log: {result.get('content')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
