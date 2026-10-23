import json
import os
from datetime import datetime, timezone

import requests


def write_structured_log(message, severity="INFO", **fields):
    api_key = os.environ.get("DATADOG_API_KEY")
    site = os.environ.get("DATADOG_SITE", "datadoghq.com")
    if not api_key:
        raise RuntimeError("DATADOG_API_KEY is required")

    url = f"https://http-intake.logs.{site}/api/v2/logs"
    payload = {
        "ddsource": "python",
        "service": fields.pop("service", "application"),
        "status": severity.lower(),
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **fields,
    }

    response = requests.post(
        url,
        headers={
            "DD-API-KEY": api_key,
            "Content-Type": "application/json",
        },
        data=json.dumps([payload]),
        timeout=10,
    )
    response.raise_for_status()
    return {"submitted": True, "status_code": response.status_code}
