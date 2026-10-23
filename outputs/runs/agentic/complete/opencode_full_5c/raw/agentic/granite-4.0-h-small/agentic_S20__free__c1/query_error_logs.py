import time
import json
import requests
from observability_client import get_log_service_url, get_auth_header


def query_error_logs(start_time: int, end_time: int, severity: str = "ERROR"):
    """Query recent error log entries filtered by severity and time range.

    Provider: Splunk Search Processing Language (SPL)
    """
    url = get_log_service_url() + "/search"
    headers = {
        **get_auth_header(),
        "Content-Type": "application/json",
    }
    payload = {
        "query": f"index=main severity={severity} | where _time >= {start_time} AND _time <= {end_time}"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()
