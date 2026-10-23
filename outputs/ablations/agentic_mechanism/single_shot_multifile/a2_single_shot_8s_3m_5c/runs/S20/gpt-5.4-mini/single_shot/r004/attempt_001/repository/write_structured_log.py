import os
import uuid
from datetime import datetime, timezone
from observability_client import get_logger_client, resolve_log_name
from observability_models import normalize_log_event, build_structured_payload


def main():
    client = get_logger_client()
    log_name = resolve_log_name()
    event = normalize_log_event(
        build_structured_payload(
            message="structured application event",
            severity="INFO",
            fields={"event_type": "structured", "service": "api", "status": "ok"},
            request_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
        )
    )
    client.write(log_name=log_name, payload=event)


if __name__ == "__main__":
    main()
