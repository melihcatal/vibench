import json
import uuid
from datetime import datetime, timezone
from observability_client import get_log_client, resolve_log_source
from observability_models import LogEvent, build_batch_log_payload, normalize_event


def main() -> dict:
    client = get_log_client()
    correlation_id = str(uuid.uuid4())
    source = resolve_log_source("correlated-logs")
    events = [
        LogEvent(
            message="request received",
            severity="INFO",
            timestamp=datetime.now(timezone.utc).isoformat(),
            service="payments-api",
            source=source,
            correlation_id=correlation_id,
            fields={"step": "ingress", "path": "/authorize"},
        ),
        LogEvent(
            message="request completed",
            severity="INFO",
            timestamp=datetime.now(timezone.utc).isoformat(),
            service="payments-api",
            source=source,
            correlation_id=correlation_id,
            fields={"step": "egress", "status_code": 200},
        ),
    ]
    payload = build_batch_log_payload([normalize_event(e) for e in events])
    response = client.write_log(payload)
    return {"status": response.status, "request_id": response.request_id, "correlation_id": correlation_id}


if __name__ == "__main__":
    print(json.dumps(main()))
