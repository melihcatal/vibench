import json
import os
from datetime import datetime, timezone

import requests


def write_structured_log(event_name: str, severity: str, payload: dict) -> dict:
    api_key = os.environ["DYNATRACE_API_TOKEN"]
    environment_id = os.environ["DYNATRACE_ENVIRONMENT_ID"]
    endpoint = f"https://{environment_id}.live.dynatrace.com/api/v2/logs/ingest"
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_name": event_name,
        "severity": severity,
        "payload": payload,
        "provider": "dynatrace",
    }
    response = requests.post(
        endpoint,
        headers={
            "Authorization": f"Api-Token {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps([record]),
        timeout=10,
    )
    response.raise_for_status()
    return record


if __name__ == "__main__":
    write_structured_log(
        event_name="structured_log_written",
        severity="INFO",
        payload={"status": "ok"},
    )
