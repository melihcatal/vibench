import os
from observability_client import create_client, load_config
from observability_models import normalize_event


def main() -> None:
    client = create_client()
    cfg = load_config()
    correlation_id = os.getenv("CORRELATION_ID", "corr-abc-001")
    events = [
        normalize_event(
            {
                "severity": "INFO",
                "message": "request received",
                "correlation_id": correlation_id,
                "stage": "ingress",
            }
        ),
        normalize_event(
            {
                "severity": "INFO",
                "message": "payment authorized",
                "correlation_id": correlation_id,
                "stage": "processing",
            }
        ),
        normalize_event(
            {
                "severity": "INFO",
                "message": "request completed",
                "correlation_id": correlation_id,
                "stage": "egress",
            }
        ),
    ]
    for event in events:
        client.index(index=f"{cfg.index_prefix}-app", body=event)


if __name__ == "__main__":
    main()
