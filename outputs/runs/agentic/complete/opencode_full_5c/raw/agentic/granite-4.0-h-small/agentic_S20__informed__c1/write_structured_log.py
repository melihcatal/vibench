import json
import os
from observability_client import get_log_client


def write_structured_log(message: str, level: str = "info", **context):
    """Write a JSON log event to the configured managed logging service.

    The function uses the default log client (e.g., Google Cloud Logging,
    CloudWatch, Datadog, etc.) and sends a structured log with a severity
    field and optional key‑value attributes.
    """
    # Normalise context to ensure no private keys are logged
    normalized = {k: v for k, v in context.items() if not k.startswith("_")}
    log_entry = {
        "timestamp": os.getenv("LOG_TIMESTAMP", "2024-01-01T00:00:00Z"),
        "level": level,
        "message": message,
        **normalized,
    }
    client = get_log_client()
    client.log_structured(log_entry)
