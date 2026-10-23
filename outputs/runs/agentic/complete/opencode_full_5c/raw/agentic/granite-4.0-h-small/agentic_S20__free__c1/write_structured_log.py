import json
import requests
from observability_client import get_log_service_url, get_auth_header


def write_structured_log(event_id: str, message: str, severity: str, request_id: str):
    """Write a structured JSON log event to the managed logging service.

    Provider: Splunk HTTP Event Collector (HEC)
    """
    url = get_log_service_url()
    headers = {
        **get_auth_header(),
        "Content-Type": "application/json",
    }
    payload = {
        "event": {
            "event_id": event_id,
            "message": message,
            "severity": severity,
            "request_id": request_id,
            "timestamp": int(round(time.time() * 1000)),
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()
