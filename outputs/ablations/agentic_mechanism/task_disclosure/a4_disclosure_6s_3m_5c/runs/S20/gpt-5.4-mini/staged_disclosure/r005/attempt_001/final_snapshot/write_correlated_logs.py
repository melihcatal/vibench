import json
import os
import uuid
from datetime import datetime, timezone

import requests


def build_correlated_events(request_id: str):
    timestamp = datetime.now(timezone.utc).isoformat()
    return [
        {
            "provider": "postman-echo",
            "service": "web-app",
            "event": "request_received",
            "request_id": request_id,
            "timestamp": timestamp,
        },
        {
            "provider": "postman-echo",
            "service": "web-app",
            "event": "database_query_completed",
            "request_id": request_id,
            "timestamp": timestamp,
        },
        {
            "provider": "postman-echo",
            "service": "web-app",
            "event": "response_sent",
            "request_id": request_id,
            "timestamp": timestamp,
        },
    ]


def send_log_event(event):
    api_key = os.environ.get("POSTMAN_ECHO_API_KEY", "")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-Api-Key"] = api_key
    return requests.post("https://postman-echo.com/post", headers=headers, json=event, timeout=30)


def main():
    request_id = str(uuid.uuid4())
    events = build_correlated_events(request_id)
    results = []
    for event in events:
        response = send_log_event(event)
        results.append({"status_code": response.status_code, "body": response.text})
    print(json.dumps({"request_id": request_id, "results": results}, indent=2))


if __name__ == "__main__":
    main()
