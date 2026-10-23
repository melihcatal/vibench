import time
from observability_client import get_log_client
import json

# Using Datadog Logs API as the concrete managed logging service

def write_structured_log(log_entry: dict) -> None:
    """Write a structured JSON log event to Datadog Logs.

    Args:
        log_entry (dict): The log payload, already in JSON‑serializable form.
    """
    client = get_log_client()
    payload = json.dumps(log_entry)
    response = client.Logs.send(payload)
    if response.status_code != 202:
        raise RuntimeError(f"Failed to write log: {response.text}")
    print(f"Structured log written at {time.time()}.")


def write_correlated_logs(logs: list, correlation_id: str) -> None:
    """Write a collection of log events that share a common correlation identifier.

    Args:
        logs (list): List of dict log entries, each will receive the same 'correlation_id' field.
        correlation_id (str): The request or request‑id to attach to every log.
    """
    client = get_log_client()
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


def query_error_logs(start_time: int, end_time: int, severity: str = 'error') -> list:
    """Query recent error log entries from the managed logging service.

    Args:
        start_time (int): Unix epoch milliseconds – beginning of the window.
        end_time (int): Unix epoch milliseconds – end of the window.
        severity (str): Log level to filter on (default 'error').

    Returns:
        list: Parsed log records matching the criteria.
    """
    client = get_log_client()
    query = f"@timestamp:>{start_time} AND @timestamp:<{end_time} AND @log_stream:error"
    response = client.Logs.query(query=query, start=start_time, end=end_time)
    if response.status_code != 200:
        raise RuntimeError(f"Query failed: {response.text}")
    return response.json()


def fetch_recent_logs(field: str, value: str, start_time: int, end_time: int) -> list:
    """Retrieve recent log entries filtered by a specific field/value and time range.

    Args:
        field (str): Log field name to filter on (e.g., 'environment').
        value (str): Expected field value.
        start_time (int): Unix epoch ms for window start.
        end_time (int): Unix epoch ms for window end.

    Returns:
        list: List of log records matching the criteria.
    """
    client = get_log_client()
    query = f"@{field}:{value} AND @timestamp:>{start_time} AND @timestamp:<{end_time}"
    response = client.Logs.query(query=query, start=start_time, end=end_time)
    if response.status_code != 200:
        raise RuntimeError(f"Fetch failed: {response.text}")
    return response.json()
