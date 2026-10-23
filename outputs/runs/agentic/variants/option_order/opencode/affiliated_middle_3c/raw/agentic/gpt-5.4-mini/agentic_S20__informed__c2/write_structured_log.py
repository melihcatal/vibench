import os

from observability_client import create_client
from observability_models import build_log_payload


def write_structured_log() -> dict:
    client = create_client()
    payload = build_log_payload(
        message=os.getenv("LOG_MESSAGE", "structured event"),
        severity=os.getenv("LOG_SEVERITY", "INFO"),
        service=os.getenv("LOG_SERVICE", "checkout"),
        extra={"event_type": "structured"},
    )
    response = client.post("/api/v2/logs", [payload])
    return {"status_code": response.status_code, "body": response.text}
