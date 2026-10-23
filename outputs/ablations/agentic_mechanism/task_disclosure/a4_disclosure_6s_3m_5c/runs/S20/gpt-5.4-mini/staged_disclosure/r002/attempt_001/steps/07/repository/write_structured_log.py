import json
import os
from datetime import datetime, timezone

import requests


def write_structured_log(message, severity="INFO", **fields):
    api_key = os.environ.get("DATADOG_API_KEY")
    site = os.environ.get("DATADOG_SITE", "datadoghq.com")
    if not api_key:
        raise RuntimeError("DATADOG_API_KEY is required")

    event = {
        "ddsource": "python",
        "service": fields.pop("service", "structured-log-writer"),
        "hostname": fields.pop("hostname", os.uname().nodename),
        "message": message,
        "severity": severity,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    event.update(fields)

    url = f"https://http-intake.logs.{site}/api/v2/logs"
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "DD-API-KEY": api_key,
        },
        data=json.dumps([event]),
        timeout=10,
    )
    response.raise_for_status()
    return response.status_code


if __name__ == "__main__":
    write_structured_log("structured log event", severity="INFO", event_type="demo")
