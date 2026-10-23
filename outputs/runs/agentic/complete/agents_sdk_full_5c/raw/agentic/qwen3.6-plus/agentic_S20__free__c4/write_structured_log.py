"""
Writes a structured JSON log event to a managed logging service.

Uses the Datadog Logs API (api.datadoghq.com) via the datadog-api-client SDK
to ingest a structured log event with the HTTPLog/HTTPLogs model.
"""

from __future__ import annotations

import json
import sys
import os
from typing import Any, Dict, Optional

from observability_models import StructuredLogEvent, LogLevel, generate_correlation_id
from observability_client import ingest_log_event, load_datadog_config

DATADOG_API_HOST = "https://api.datadoghq.com"


def write_structured_log(
    message: str,
    service: str,
    environment: str = "production",
    level: str = "info",
    correlation_id: Optional[str] = None,
    tags: Optional[list] = None,
    custom_attributes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Write a single structured JSON log event to Datadog.

    The log event is sent to the Datadog managed logging service
    at api.datadoghq.com using the v2 HTTP Logs ingestion endpoint
    with the datadog-api-client Python SDK.

    Args:
        message: The log message content.
        service: The service name emitting the log.
        environment: Deployment environment (e.g., production, staging).
        level: Log severity level (debug, info, warning, error, critical).
        correlation_id: Optional correlation/tracing ID.
        tags: Optional list of tags for the log event.
        custom_attributes: Additional key-value pairs to include in the log.

    Returns:
        Dict with ingestion status and event metadata.
    """
    normalized_level = LogLevel(level.lower()) if isinstance(level, str) else level

    event = StructuredLogEvent(
        message=message,
        service=service,
        environment=environment,
        level=normalized_level,
        correlation_id=correlation_id or generate_correlation_id("log"),
        tags=tags or [],
        custom_attributes=custom_attributes or {},
    )

    result = ingest_log_event(event)
    result["level"] = event.level.value
    result["service"] = event.service
    result["environment"] = event.environment
    return result


def main() -> None:
    """CLI entry point for writing a structured log to Datadog."""
    message = os.environ.get("LOG_MESSAGE", "Structured log test event")
    service = os.environ.get("LOG_SERVICE", "my-application")
    environment = os.environ.get("LOG_ENVIRONMENT", "production")
    level = os.environ.get("LOG_LEVEL", "info")
    tags_str = os.environ.get("LOG_TAGS", "")
    tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else []

    result = write_structured_log(
        message=message,
        service=service,
        environment=environment,
        level=level,
        tags=tags,
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
