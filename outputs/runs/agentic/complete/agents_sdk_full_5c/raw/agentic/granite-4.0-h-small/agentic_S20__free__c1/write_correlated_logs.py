import time
from observability_client import get_log_client

# Using Datadog Timeboard/Logs API as the concrete managed logging service

def write_correlated_logs(logs: list, correlation_id: str) -> None:
    """Write a collection of log events that share a common correlation identifier.

    Args:
        logs (list): List of dict log entries, each will receive the same 'correlation_id' field.
        correlation_id (str): The request or request-id to attach to every log.
    """
    client = get_log_client()
    # Add the correlation identifier to each log
    enriched_logs = []
    for log in logs:
        enriched = log.copy()
        enriched['correlation_id'] = correlation_id
        enriched_logs.append(enriched)

    payload = json.dumps(enriched_logs)
    response = client.Logs.send(payload)
    if response.status_code != 202:
        raise RuntimeError(f"Failed to write correlated logs: {response.text}")
    print(f"{len(logs)} correlated logs written at {time.time()}.")
