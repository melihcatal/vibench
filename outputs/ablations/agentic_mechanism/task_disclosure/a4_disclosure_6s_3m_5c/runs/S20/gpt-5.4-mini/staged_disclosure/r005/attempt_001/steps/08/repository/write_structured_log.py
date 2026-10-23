import json
import os
import uuid
from datetime import datetime, timezone

import requests


def write_structured_log(message: str, severity: str = "INFO", **fields):
    service = os.getenv("CLOUD_LOGGING_SERVICE", "google_cloud_logging")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    api_key = os.getenv("GOOGLE_CLOUD_API_KEY")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    if not api_key:
        raise ValueError("GOOGLE_CLOUD_API_KEY is required")

    event = {
        "insertId": str(uuid.uuid4()),
        "jsonPayload": {
            "service": service,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **fields,
        },
    }

    url = f"https://logging.googleapis.com/v2/projects/{project_id}/logs:write"
    response = requests.post(
        url,
        params={"key": api_key},
        headers={"Content-Type": "application/json"},
        data=json.dumps(event),
        timeout=30,
    )
    response.raise_for_status()
    return response.json() if response.content else None
