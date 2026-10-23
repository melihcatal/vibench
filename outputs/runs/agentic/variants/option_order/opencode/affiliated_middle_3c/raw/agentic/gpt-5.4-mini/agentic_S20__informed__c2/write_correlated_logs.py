import os
import uuid

from observability_client import create_client
from observability_models import build_log_payload


def write_correlated_logs() -> dict:
    client = create_client()
    correlation_id = os.getenv("CORRELATION_ID", str(uuid.uuid4()))
    events = [
        build_log_payload(
            "request received", "INFO", "api", correlation_id, {"step": "start"}
        ),
        build_log_payload(
            "request completed", "INFO", "api", correlation_id, {"step": "end"}
        ),
    ]
    response = client.post("/api/v2/logs", events)
    return {
        "status_code": response.status_code,
        "body": response.text,
        "correlation_id": correlation_id,
    }
