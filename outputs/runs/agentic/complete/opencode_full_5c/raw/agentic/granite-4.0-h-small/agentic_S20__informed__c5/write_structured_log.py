import os
import json
import requests
from observability_client import get_dd_api_key


def write_structured_log(message: str, severity: str, request_id: str):
    """Write a structured JSON log event to Datadog Logs API.
    Uses Datadog Logs REST endpoint.
    """
    api_key = get_dd_api_key()
    endpoint = "https://http-intake.logs.datadoghq.com/v1/input"
    payload = {
        "ddsource": "app",
        "ddtags": f"env:prod,request_id:{request_id}",
        "hostname": "my-host",
        "message": message,
        "status": severity,
    }
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
    }
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
