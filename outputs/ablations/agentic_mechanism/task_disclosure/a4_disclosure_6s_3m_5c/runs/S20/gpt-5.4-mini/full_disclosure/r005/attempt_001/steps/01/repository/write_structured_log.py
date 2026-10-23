import json
import os
from datetime import datetime, timezone

import requests


DATADOG_URL = os.getenv("DATADOG_LOGS_API_URL", "https://http-intake.logs.datadoghq.com/api/v2/logs")
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")


def write_structured_log(message, service=None, level="info", **fields):
    if not DATADOG_API_KEY:
        raise ValueError("DATADOG_API_KEY is required")

    payload = {
        "ddsource": "python",
        "service": service or os.getenv("DD_SERVICE", "app"),
        "status": level,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    payload.update(fields)

    response = requests.post(
        DATADOG_URL,
        headers={
            "DD-API-KEY": DATADOG_API_KEY,
            "Content-Type": "application/json",
        },
        data=json.dumps([payload]),
        timeout=10,
    )
    response.raise_for_status()
    return {"status_code": response.status_code, "provider": "datadog"}


if __name__ == "__main__":
    raise SystemExit(0)
