import os
import requests
from datetime import datetime, timedelta

# Using Datadog Logs (https://www.datadoghq.com) as the managed logging service
# Requires DD_API_KEY environment variable

def query_error_logs(severity: str = "error", start_relative: int = 3600) -> dict:
    """
    Query Datadog for recent error logs.
    Args:
        severity (str): Log level to filter (default 'error').
        start_relative (int): Seconds before now to include.
    Returns:
        dict: API response with log hits.
    """
    api_key = os.getenv("DD_API_KEY")
    if not api_key:
        raise RuntimeError("DD_API_KEY not set")
    now_iso = datetime.utcnow().isoformat() + "Z"
    start_iso = (datetime.utcnow() - timedelta(seconds=start_relative)).isoformat() + "Z"
    query = f"@severity:{severity}"
    url = "https://api.datadoghq.com/api/v1/logs/queries?api_key={}&application_key={}&start={}&end={}&query={}&priority=normal"
    # Use the same key for application_key placeholder
    url = url.format(api_key, api_key, start_iso, now_iso, query)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()