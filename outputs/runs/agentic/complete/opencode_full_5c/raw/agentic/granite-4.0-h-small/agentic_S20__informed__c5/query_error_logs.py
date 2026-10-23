import os
import datetime
from datetime import timezone
import requests
from observability_client import get_ibm_cloud_api_key, get_ibm_logs_instance_id


def query_error_logs(severity: str = "error", minutes_back: int = 60):
    """Query recent error logs from IBM Cloud Logs using the REST API.
    Returns a list of matching log records.
    Parameters:
        severity (str): Log severity level to filter on.
        minutes_back (int): Lookback window in minutes from now.
    """
    api_key = get_ibm_cloud_api_key()
    instance_id = get_ibm_logs_instance_id()
    now = datetime.datetime.now(timezone.utc)
    start_time = (now - datetime.timedelta(minutes=minutes_back)).isoformat()
    endpoint = f"https://<region>.logs.<service>.ibmcloud.com/api/v1/logs?instance_id={instance_id}&start_time={start_time}"
    params = {"query": f"severity:{severity}"}
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
