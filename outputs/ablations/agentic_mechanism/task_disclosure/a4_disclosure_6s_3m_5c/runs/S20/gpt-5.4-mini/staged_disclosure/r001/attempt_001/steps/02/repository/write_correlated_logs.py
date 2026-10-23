import json
import os
import sys
import time
import uuid

import requests


NEW_RELIC_INGEST_URL = "https://log-api.newrelic.com/log/v1"


def build_events(correlation_id: str):
    now = int(time.time() * 1000)
    return [
        {
            "timestamp": now,
            "message": "request started",
            "level": "INFO",
            "service.name": os.getenv("SERVICE_NAME", "example-app"),
            "request.id": correlation_id,
            "correlation.id": correlation_id,
        },
        {
            "timestamp": now + 10,
            "message": "request completed",
            "level": "INFO",
            "service.name": os.getenv("SERVICE_NAME", "example-app"),
            "request.id": correlation_id,
            "correlation.id": correlation_id,
        },
    ]


def send_logs(events):
    license_key = os.getenv("NEW_RELIC_LICENSE_KEY")
    if not license_key:
        raise RuntimeError("NEW_RELIC_LICENSE_KEY is required")
    headers = {
        "Api-Key": license_key,
        "Content-Type": "application/json",
    }
    response = requests.post(NEW_RELIC_INGEST_URL, headers=headers, data=json.dumps(events), timeout=30)
    response.raise_for_status()


def main():
    correlation_id = os.getenv("CORRELATION_ID", str(uuid.uuid4()))
    events = build_events(correlation_id)
    send_logs(events)
    sys.stdout.write(correlation_id + "\n")


if __name__ == "__main__":
    main()
