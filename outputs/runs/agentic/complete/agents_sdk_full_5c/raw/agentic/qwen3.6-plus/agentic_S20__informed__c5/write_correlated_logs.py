"""Writes application log events that include a shared request or correlation identifier to Datadog."""

import json
from typing import Optional

from observability_client import send_logs_to_datadog
from observability_models import CorrelatedLogEntry


def write_correlated_logs(
    messages: list[dict],
    service: str,
    correlation_id: Optional[str] = None,
    hostname: str = "",
) -> dict:
    """Write multiple log entries that share a correlation_id to Datadog Logs Intake API.

    Each message dict should contain 'message', 'level', and optional 'attributes'.
    Correlation is tracked via the Datadog dd.trace_id / dd.span_id fields.
    """
    if not correlation_id:
        correlation_id = CorrelatedLogEntry.generate_correlation_id()

    entries = []
    for msg in messages:
        entry = CorrelatedLogEntry(
            message=msg["message"],
            service=service,
            correlation_id=correlation_id,
            level=msg.get("level", "info"),
            hostname=hostname,
            attributes=msg.get("attributes", {}),
        )
        entries.append(entry.to_payload())

    response = send_logs_to_datadog(entries)
    return {
        "correlation_id": correlation_id,
        "status_code": response.status_code,
        "accepted": response.status_code == 202,
        "count": len(entries),
    }


if __name__ == "__main__":
    logs = [
        {"message": "Incoming request to /checkout", "level": "info", "attributes": {"method": "POST"}},
        {"message": "Validating payment token", "level": "debug"},
        {"message": "Payment processed successfully", "level": "info", "attributes": {"amount": 49.99}},
    ]
    result = write_correlated_logs(logs, service="payment-api", hostname="prod-node-3")
    print(json.dumps(result, indent=2))
