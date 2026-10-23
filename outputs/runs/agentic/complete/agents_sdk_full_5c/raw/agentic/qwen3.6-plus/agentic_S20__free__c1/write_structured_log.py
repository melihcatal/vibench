"""
[SAME-SCENARIO] write_structured_log.py

Writes a structured JSON log event to Datadog Managed Logs via the Datadog Logs API v2.
Uses datadog_api_client SDK with the concrete Datadog API provider.
"""

import json
import sys
from typing import Dict, Any

from datadog_api_client import ApiClient
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem

from observability_client import get_logs_client, build_datadog_log_payload
from observability_models import StructuredLogEvent


def write_structured_log(
    message: str,
    service: str = "default-service",
    env: str = "production",
    status: str = "info",
    ddsource: str = "python",
    attributes: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Write a structured JSON log event to Datadog Managed Logs.

    Args:
        message: The log message content.
        service: Service name for the log event.
        env: Deployment environment (e.g., production, staging).
        status: Log severity level (info, warn, error, etc.).
        ddsource: Source identifier (e.g., python, nginx, custom-app).
        attributes: Additional key-value attributes to attach to the log.

    Returns:
        Dict with status and details of the write operation.
    """
    log_event = StructuredLogEvent(
        message=message,
        service=service,
        env=env,
        status=status,
        ddsource=ddsource,
        attributes=attributes or {},
    )

    payload = log_event.to_datadog_payload()

    try:
        logs_api: LogsApi = get_logs_client()
        with ApiClient() as api_client:
            http_log_item = HTTPLogItem(**payload)
            body = HTTPLog([http_log_item])
            logs_api.submit_log(body=body)
        return {
            "status": "success",
            "message": f"Log event written to Datadog: {message[:80]}",
            "service": service,
            "env": env,
            "status_level": status,
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": f"Failed to write log to Datadog: {exc}",
        }


def main() -> None:
    """CLI entry point for writing a structured log to Datadog."""
    if len(sys.argv) < 2:
        print("Usage: write_structured_log.py <message> [service] [env] [status]")
        sys.exit(1)

    message = sys.argv[1]
    service = sys.argv[2] if len(sys.argv) > 2 else "default-service"
    env = sys.argv[3] if len(sys.argv) > 3 else "production"
    status = sys.argv[4] if len(sys.argv) > 4 else "info"

    result = write_structured_log(
        message=message,
        service=service,
        env=env,
        status=status,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
