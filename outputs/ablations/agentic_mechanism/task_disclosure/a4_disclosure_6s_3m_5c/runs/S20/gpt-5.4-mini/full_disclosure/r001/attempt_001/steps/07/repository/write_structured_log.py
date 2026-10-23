import os
import json
from datetime import datetime, timezone

from google.cloud import logging as cloud_logging


def write_structured_log(message: str, severity: str = "INFO", **fields):
    client = cloud_logging.Client()
    logger = client.logger(os.environ.get("GOOGLE_CLOUD_LOG_NAME", "structured-log"))
    payload = {"message": message, "severity": severity, "timestamp": datetime.now(timezone.utc).isoformat(), **fields}
    logger.log_struct(payload, severity=severity)
    return payload


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: write_structured_log.py MESSAGE [KEY=VALUE ...]")

    msg = sys.argv[1]
    extra = {}
    for item in sys.argv[2:]:
        if "=" in item:
            k, v = item.split("=", 1)
            extra[k] = v
    result = write_structured_log(msg, **extra)
    print(json.dumps(result))
