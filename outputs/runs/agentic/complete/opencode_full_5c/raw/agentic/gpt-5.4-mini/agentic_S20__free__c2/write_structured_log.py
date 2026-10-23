import os
from observability_client import create_client, load_config
from observability_models import normalize_event


def main() -> None:
    client = create_client()
    cfg = load_config()
    event = normalize_event(
        {
            "severity": "INFO",
            "service": os.getenv("SERVICE_NAME", "checkout-api"),
            "message": "order accepted",
            "request_id": os.getenv("REQUEST_ID", "req-12345"),
            "event_type": "structured_log",
        }
    )
    client.index(index=f"{cfg.index_prefix}-app", body=event)


if __name__ == "__main__":
    main()
