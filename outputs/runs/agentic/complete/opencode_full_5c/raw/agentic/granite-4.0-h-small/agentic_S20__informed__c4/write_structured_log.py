import json
import os
from observability_client import get_log_client


def write_structured_log(
    message: str, severity: str = "info", correlation_id: str | None = None
):
    """Write a structured JSON log event to the chosen managed logging service.

    Uses the configured provider client from observability_client.py.
    """
    client = get_log_client()
    log_event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": message,
        "severity": severity,
        "correlationId": correlation_id,
    }
    try:
        response = client.log_ingest(log_event)
        print(f"Ingested log: {response}")
    except Exception as e:
        print(f"Failed to ingest log: {e}")
