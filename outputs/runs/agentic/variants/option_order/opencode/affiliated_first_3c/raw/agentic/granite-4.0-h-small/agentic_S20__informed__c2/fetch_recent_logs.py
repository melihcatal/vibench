# [SAME-SCENARIO] fetch_recent_logs.py
"""Retrieve recent log results filtered by field values and time range."""

import datetime
from observability_client import get_logging_client


def fetch_recent_logs(
    severity: str = "info",
    field_value: str = None,
    start_time: str = None,
    end_time: str = None,
):
    """Fetch recent logs filtered by fields and time.

    Args:
        severity (str): Severity filter.
        field_value (str): Value of a specific field to match.
        start_time (str): Start timestamp ISO8601.
        end_time (str): End timestamp ISO8601.
    """
    client = get_logging_client()
    # Example using Azure Monitor Logs query via SDK
    query = (
        f'AzureDiagnostics | where severityLevel == "{severity}"'
        + (f' and field == "{field_value}"' if field_value else "")
        + f" | where TimeGenerated between (datetime({start_time}) .. datetime({end_time}))"
        if start_time and end_time
        else ""
    )
    response = client.query(query=query)
    return response.get("tables", [{}])[0].get("rows", [])
