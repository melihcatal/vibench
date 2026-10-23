import uuid
from datetime import datetime, timezone
from observability_client import get_logger_client, resolve_log_name
from observability_models import normalize_log_event, build_correlated_payload


def main():
    client = get_logger_client()
    log_name = resolve_log_name()
    correlation_id = str(uuid.uuid4())
    payloads = [
        build_correlated_payload(
            message="request received",
            severity="INFO",
            correlation_id=correlation_id,
            step="received",
            timestamp=datetime.now(timezone.utc),
        ),
        build_correlated_payload(
            message="request processed",
            severity="INFO",
            correlation_id=correlation_id,
            step="processed",
            timestamp=datetime.now(timezone.utc),
        ),
    ]
    for payload in payloads:
        client.write(log_name=log_name, payload=normalize_log_event(payload))


if __name__ == "__main__":
    main()
