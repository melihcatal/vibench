"""
Writes a structured JSON log event to Datadog managed logging service.

Uses the Datadog Logs Ingestion API (api.datadoghq.com) via the requests library.
Auth: DD_API_KEY, DD_APP_KEY environment variables.
"""

import json
import os
import sys
from datetime import datetime, timezone

from observability_client import create_datadog_session, send_log_to_datadog
from observability_models import LogEvent


def write_structured_log(
    message: str,
    service: str = "default",
    status: str = "info",
    tags: str = "",
    attributes: dict | None = None,
) -> dict:
    """Write a single structured JSON log event to Datadog Logs.

    The log is sent to the Datadog Logs Ingestion API endpoint at
    api.datadoghq.com/api/v2/logs with Datadog-specific headers
    (DD-API-KEY, DD-APPLICATION-KEY).
    """
    session = create_datadog_session()

    event = LogEvent(
        message=message,
        service=service,
        status=status,
        ddtags=tags,
        attributes=attributes or {},
    )

    result = send_log_to_datadog(session, event)
    return result


def main():
    """Entry point for writing a structured log event to Datadog."""
    message = os.environ.get("LOG_MESSAGE", "Structured log event from Python")
    service = os.environ.get("LOG_SERVICE", "sample-service")
    status = os.environ.get("LOG_STATUS", "info")
    tags = os.environ.get("LOG_TAGS", "env:production,team:platform")

    attributes = {
        "event_type": "structured_log",
        "language": "python",
        "log_version": "1.0",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }

    result = write_structured_log(
        message=message,
        service=service,
        status=status,
        tags=tags,
        attributes=attributes,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
