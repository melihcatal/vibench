import uuid
import json
from observability_client import get_log_client


def write_correlated_logs(message: str, severity: str = "info"):
    """Write application log events that include a shared request/correlation identifier.

    Generates a UUID v4 correlation ID if none is supplied by the caller.
    """
    correlation_id = uuid.uuid4().hex
    client = get_log_client()
    log_event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": message,
        "severity": severity,
        "correlationId": correlation_id,
    }
    try:
        response = client.log_ingest(log_event)
        print(f"Ingested correlated log: {response}")
    except Exception as e:
        print(f"Failed to ingest log: {e}")
