import json
import os
from observability_client import get_log_client


def write_correlated_logs(
    message: str, correlation_id: str, level: str = "info", **context
):
    """Write one or more JSON log events that share a common request identifier.

    This helper demonstrates how to include a shared `correlation_id` field in
    every log emitted by a single request or transaction. The underlying client
    is the same managed logging service used by write_structured_log.
    """
    normalized = {k: v for k, v in context.items() if not k.startswith("_")}
    log_entry = {
        "timestamp": os.getenv("LOG_TIMESTAMP", "2024-01-01T00:00:00Z"),
        "level": level,
        "message": message,
        "correlation_id": correlation_id,
        **normalized,
    }
    client = get_log_client()
    client.log_structured(log_entry)
