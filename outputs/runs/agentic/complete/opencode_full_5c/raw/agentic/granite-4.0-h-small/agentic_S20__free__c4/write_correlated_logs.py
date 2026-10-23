import json
from observability_client import get_log_client


def write_correlated_logs(
    log_batch: list[dict], correlation_id: str, log_service: str = "datadog"
) -> None:
    """Write application log events that include a shared correlation identifier.

    Args:
        log_batch: List of log dictionaries to send.
        correlation_id: Identifier shared across the batch (e.g., request ID).
        log_service: Logging provider identifier (default: "datadog").
    """
    client = get_log_client(log_service)
    for log in log_batch:
        # Add correlation ID if not already present
        log.setdefault("correlation_id", correlation_id)
    payload = json.dumps(log_batch)
    response = client.create_log(payload)
    print(f"Correlated logs sent to {log_service} (ID={correlation_id}): {response}")
