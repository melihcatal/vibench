import time
import json
import requests
from observability_client import get_log_service_url, get_auth_header


def fetch_recent_logs(start_time: int, end_time: int, field_filters: dict = None):
    """Retrieve recent log results filtered by field values and time range.

    Provider: Splunk Search Processing Language (SPL)
    """
    url = get_log_service_url() + "/search"
    headers = {
        **get_auth_header(),
        "Content-Type": "application/json",
    }
    query = f"index=main _time >= {start_time} AND _time <= {end_time}"
    if field_filters:
        conditions = [f"{field}={value}" for field, value in field_filters.items()]
        query += " AND " + " AND ".join(conditions)
    payload = {"query": query}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()
