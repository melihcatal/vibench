import uuid
import time
import json
import requests
from observability_client import get_log_service_url, get_auth_header


def write_correlated_logs(request_id: str, logs: list[dict]):
    """Write multiple application log events that share a request/correlation identifier.

    Provider: Splunk HTTP Event Collector (HEC)
    """
    url = get_log_service_url()
    headers = {**get_auth_header(), "Content-Type": "application/json"}
    payload = {
        "events": [
            {
                "event_id": str(uuid.uuid4()),
                "message": log.get("message"),
                "severity": log.get("severity"),
                "request_id": request_id,
                "timestamp": int(log.get("timestamp", time.time() * 1000)),
            }
            for log in logs
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()
