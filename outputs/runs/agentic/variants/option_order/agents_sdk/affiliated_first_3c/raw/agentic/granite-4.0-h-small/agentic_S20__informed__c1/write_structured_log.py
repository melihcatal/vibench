import json
from observability_client import get_client

def write_structured_log(resource_id: str, message: str, level: str = "info", tags: list = None):
    """Write a structured JSON log event to IBM Cloud Logs.

    Args:
        resource_id: Resource identifier for the log entry.
        message: Log message text.
        level: Severity level (info, error, warn, etc.).
        tags: Optional list of key-value pairs.
    """
    client = get_client()
    log_entry = {
        "timestamp": client.now_iso(),
        "resource_id": resource_id,
        "message": message,
        "level": level,
        "tags": tags or {},
    }
    # Send log via HTTP REST endpoint
    response = client.post("/v1/logs", json=log_entry)
    response.raise_for_status()
    print(f"Log sent: {log_entry}")
