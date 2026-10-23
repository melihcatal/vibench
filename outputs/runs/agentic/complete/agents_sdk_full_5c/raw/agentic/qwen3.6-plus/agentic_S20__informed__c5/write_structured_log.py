"""Writes a structured JSON log event to Datadog Logs API."""

import json
from typing import Optional

from observability_client import send_logs_to_datadog
from observability_models import StructuredLogEntry


def write_structured_log(
    message: str,
    service: str,
    level: str = "info",
    hostname: str = "",
    attributes: Optional[dict] = None,
) -> dict:
    """Write a single structured JSON log event to the Datadog Logs Intake API.

    Uses the Datadog http-intake.logs endpoint with DD-API-KEY / DD-APPLICATION-KEY auth.
    """
    entry = StructuredLogEntry(
        message=message,
        service=service,
        level=level,
        hostname=hostname,
        attributes=attributes or {},
    )
    payload = [entry.to_payload()]
    response = send_logs_to_datadog(payload)
    return {
        "status_code": response.status_code,
        "accepted": response.status_code == 202,
    }


if __name__ == "__main__":
    result = write_structured_log(
        message="Application started successfully",
        service="payment-api",
        level="info",
        attributes={"version": "2.1.0", "region": "us-east-1"},
    )
    print(json.dumps(result, indent=2))
