import json
import os
from datetime import datetime, timezone

import requests


def write_correlated_logs(message, correlation_id, severity="INFO", **fields):
    api_key = os.environ.get("DATADOG_API_KEY")
    site = os.environ.get("DATADOG_SITE", "datadoghq.com")
    if not api_key:
        raise RuntimeError("DATADOG_API_KEY is required")
    if not correlation_id:
        raise ValueError("correlation_id is required")

    url = f"https://http-intake.logs.{site}/api/v2/logs"
    payload = {
        "ddsource": "python",
        "service": fields.pop("service", "application"),
        "status": severity.lower(),
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "correlation_id": correlation_id,
        "request_id": correlation_id,
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
