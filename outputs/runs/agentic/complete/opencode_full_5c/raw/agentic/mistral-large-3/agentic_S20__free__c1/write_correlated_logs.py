import os
from datetime import datetime
from typing import Dict, Any
from observability_client import get_logging_client
from observability_models import StructuredLogEvent


def write_correlated_logs(
    service_name: str, correlation_id: str, logs: list[Dict[str, Any]]
):
    """
    Writes application log events with a shared correlation identifier to Datadog.

    Args:
        service_name: Name of the service generating the logs
        correlation_id: Shared request or correlation identifier
        logs: List of log entries, each containing 'level', 'message', and optional custom fields
    """
    client = get_logging_client()

    log_events = []
    for log in logs:
        log_event = StructuredLogEvent(
            timestamp=datetime.utcnow().isoformat() + "Z",
            service=service_name,
            level=log["level"].upper(),
            message=log["message"],
            correlation_id=correlation_id,
            **{k: v for k, v in log.items() if k not in ["level", "message"]},
        ).dict()
        log_events.append(log_event)

    # Send to Datadog HTTP logs intake with correlation context
    client.send(
        logs=log_events,
        endpoint="https://http-intake.logs.datadoghq.com/api/v2/logs",
        headers={"DD-CORRELATION-ID": correlation_id},
    )
