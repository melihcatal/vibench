import json
import os
import sys
import uuid
from datetime import datetime, timezone

import requests


def _json_default(value):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return str(value)


def write_structured_log(message, severity="INFO", **fields):
    api_key = os.environ.get("DATADOG_API_KEY")
    site = os.environ.get("DATADOG_SITE", "datadoghq.com")
    service = os.environ.get("DD_SERVICE", "application")
    if not api_key:
        raise RuntimeError("DATADOG_API_KEY is required")

    event = {
        "message": message,
        "severity": severity,
        "service": service,
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc),
    }
    event.update(fields)

    payload = {
        "ddsource": "python",
        "service": service,
        "message": json.dumps(event, default=_json_default, separators=(",", ":")),
    }

    response = requests.post(
        f"https://http-intake.logs.{site}/api/v2/logs",
        headers={
            "Content-Type": "application/json",
            "DD-API-KEY": api_key,
        },
        data=json.dumps([payload], default=_json_default),
        timeout=10,
    )
    response.raise_for_status()
    return {"sent": True, "event_id": event["event_id"]}


def main(argv=None):
    argv = sys.argv if argv is None else argv
    if len(argv) < 2:
        raise SystemExit("usage: write_structured_log.py MESSAGE [KEY=VALUE ...]")
    message = argv[1]
    extra = {}
    for item in argv[2:]:
        if "=" in item:
            key, value = item.split("=", 1)
            extra[key] = value
    result = write_structured_log(message, **extra)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
