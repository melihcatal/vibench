from __future__ import annotations

from observability_client import get_client

SERVICE = "Google Cloud Logging"
MODEL_OR_SERVICE_SIGNAL = "google.cloud.logging"


def write_correlated_logs(request_id: str = "req-2002") -> list:
    client = get_client()
    events = [
        ("INFO", "request received", {"request_id": request_id, "step": "ingress"}),
        ("INFO", "auth completed", {"request_id": request_id, "step": "auth", "user_id": "user-42"}),
        ("INFO", "request finished", {"request_id": request_id, "step": "egress", "status_code": 200}),
    ]
    return [client.write_log(severity, message, **fields).to_dict() for severity, message, fields in events]
