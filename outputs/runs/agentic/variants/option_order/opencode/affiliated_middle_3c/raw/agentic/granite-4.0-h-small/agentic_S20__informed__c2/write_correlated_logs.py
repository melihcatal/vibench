import uuid
import json
from observability_client import LogClient, LogMessage


def write_correlated_logs(correlation_id: str, logs: list[dict]) -> None:
    """Write application log events with a shared correlation identifier.

    Example use-case: tracing logs across multiple microservices for a single request.
    Uses Datadog Logs API as the concrete logging service.
    Required environment variables:
        DD_API_KEY
        DD_APP_KEY
        DD_SITE (optional, default 'datadoghq.com')
    """
    client = LogClient()  # Datadog client initialized in helper
    for entry in logs:
        entry["ddtags"] = f"correlation_id:{correlation_id}"
        entry["ddmessage"] = json.dumps(entry["message"])
        client.create_logs([entry])
