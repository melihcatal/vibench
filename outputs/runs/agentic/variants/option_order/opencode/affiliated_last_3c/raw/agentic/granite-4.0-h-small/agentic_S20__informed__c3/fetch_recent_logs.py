import datetime
import logging
import time

# Helper imports
from observability_client import ManagedLogClient

# Retrieve recent logs filtered by field values and time range


def fetch_recent_logs(
    field_name: str = None,
    field_value: str = None,
    start_time: int = None,
    end_time: int = None,
):
    """Retrieve recent log results filtered by field values and time range.

    Uses Azure Monitor Logs via REST API (requests).
    """
    # Normalize timestamps if not provided
    if start_time is None:
        start_time = int(time.time() * 1000) - 5 * 60 * 1000  # last 5 minutes
    if end_time is None:
        end_time = int(time.time() * 1000)
    # Build query URL – assumes ManagedLogClient is configured for Azure with AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET
    client = ManagedLogClient()
    endpoint = f"https://{client.log_api_host}/api/v1/logs/query"
    query = f"{field_name} = '{field_value}'" if field_name and field_value else ""
    payload = {
        "start": start_time,
        "end": end_time,
        "query": query,
    }
    response = client.rest_call(method="POST", url=endpoint, json=payload)
    # Parse and filter logs
    logs = response.get("result", [])
    if field_name and field_value:
        logs = [l for l in logs if l.get(field_name) == field_value]
    return logs
