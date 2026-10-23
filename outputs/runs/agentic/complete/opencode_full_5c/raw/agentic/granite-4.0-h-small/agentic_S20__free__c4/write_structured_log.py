import json
from observability_client import get_log_client


def write_structured_log(log_data: dict, log_service: str = "datadog") -> None:
    """Write a structured JSON log event to a managed logging service.

    Args:
        log_data: Dictionary representing the log payload.
        log_service: Identifier for the logging provider (default: "datadog").
    """
    client = get_log_client(log_service)
    # Send payload as JSON string
    response = client.create_log(json.dumps(log_data))
    print(f"Structured log sent to {log_service}: {response}")
