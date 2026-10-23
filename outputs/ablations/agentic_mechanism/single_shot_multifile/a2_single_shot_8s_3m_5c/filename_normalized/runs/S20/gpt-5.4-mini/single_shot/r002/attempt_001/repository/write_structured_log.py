import json
import os
import time
import uuid
from datetime import datetime, timezone
from observability_client import get_log_client, resolve_log_source
from observability_models import LogEvent, build_structured_log_payload, normalize_event


def main() -> dict:
    client = get_log_client()
    source = resolve_log_source("structured-log")
    event = LogEvent(
        message="structured event written",
        severity="INFO",
        timestamp=datetime.now(timezone.utc).isoformat(),
        service="checkout-api",
        source=source,
        correlation_id=str(uuid.uuid4()),
        fields={"event_type": "structured_log", "region": os.getenv("LOG_REGION", "us"), "attempt": 1},
    )
    payload = build_structured_log_payload(normalize_event(event))
    response = client.write_log(payload)
    return {"status": response.status, "request_id": response.request_id, "accepted": response.accepted}


if __name__ == "__main__":
    print(json.dumps(main()))
