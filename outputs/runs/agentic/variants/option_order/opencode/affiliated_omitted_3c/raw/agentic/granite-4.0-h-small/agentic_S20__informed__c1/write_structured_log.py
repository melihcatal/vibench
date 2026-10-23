import json
import os
from observability_client import get_ingestion_client


def write_structured_log(
    service_name: str, message: str, severity: str, request_id: str = None
):
    """Writes a structured JSON log event to a managed logging service.

    Uses the configured provider client from observability_client.
    """
    client = get_ingestion_client()
    log_event = {
        "timestamp": __timestamp(),
        "service": service_name,
        "message": message,
        "severity": severity,
        "request_id": request_id,
        "environment": os.getenv("ENVIRONMENT", "development"),
    }
    client.log(log_event)


def __timestamp():
    # Return ISO 8601 UTC string
    import datetime

    return datetime.datetime.utcnow().isoformat() + "Z"
