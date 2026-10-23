import os
import requests
from datetime import datetime, timedelta

# Using Datadog Logs (https://www.datadoghq.com) as the managed logging service
# Requires DD_API_KEY environment variable

def fetch_recent_logs(severity: str = None, fields: list = None, start_relative: int = 3600) -> dict:
    """
    Retrieve recent logs filtered by optional severity and fields.
    Args:
        severity (str): Filter by severity (e.g., 'error').
        fields (list): List of field names to return for each log entry.
        start_relative (int): Seconds ago to start the time window.
    Returns:
        dict: Parsed response containing log entries.
    """
    api_key = os.getenv("DD_API_KEY")
    if not api_key:
        raise RuntimeError("DD_API_KEY missing")
    now_iso = datetime.utcnow().isoformat() + "Z"
    start_iso = (datetime.utcnow() - timedelta(seconds=start_relative)).isoformat() + "Z"
    query = ""
    if severity:
        query += f"@severity:{severity} "
    url = "https://api.datadoghq.com/api/v1/logs/queries/fetch?api_key={}&application_key={}&start={}&end={}&priorities=normal"
    url = url.format(api_key, api_key, start_iso, now_iso)
    params = {}
    if fields:
        params["filter_by"] = ",".join(fields)
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()