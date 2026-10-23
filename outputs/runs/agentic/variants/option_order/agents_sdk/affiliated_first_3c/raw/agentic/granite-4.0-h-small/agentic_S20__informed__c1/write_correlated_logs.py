import uuid
import json
from observability_client import get_client

def write_correlated_logs(resource_id: str, message: str, correlation_id: str = None, level: str = "info"):
    """Write application log events that include a shared correlation identifier.

    Args:
        resource_id: Resource identifier for the log entry.
        message: Log message text.
        correlation_id: Optional shared correlation ID for grouping.
        level: Severity level (info, error, warn, etc.).
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    client = get_client()
    log_entry = {
        "timestamp": client.now_iso(),
        "resource_id": resource_id,
        "message": message,
        "level": level,
        "correlation_id": correlation_id,
    }
    response = client.post("/v1/logs", json=log_entry)
    response.raise_for_status()
    print(f"Correlated log sent: {log_entry}")
