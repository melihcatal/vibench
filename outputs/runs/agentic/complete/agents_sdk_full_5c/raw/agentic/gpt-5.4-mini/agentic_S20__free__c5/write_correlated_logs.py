from __future__ import annotations

from observability_client import build_openai_client, send_correlated_logs
from observability_models import LogEvent


def main() -> None:
    client = build_openai_client()
    request_id = "req-2f1c9d7a"
    correlation_id = "corr-a14d55"
    events = [
        LogEvent(
            message="Incoming request received",
            severity="INFO",
            service="api-gateway",
            request_id=request_id,
            correlation_id=correlation_id,
            fields={"path": "/v1/payments", "method": "POST"},
        ),
        LogEvent(
            message="Downstream payment service responded",
            severity="INFO",
            service="payments-worker",
            request_id=request_id,
            correlation_id=correlation_id,
            fields={"status_code": 200, "latency_ms": 84},
        ),
        LogEvent(
            message="Request completed",
            severity="INFO",
            service="api-gateway",
            request_id=request_id,
            correlation_id=correlation_id,
            fields={"status_code": 200},
        ),
    ]
    send_correlated_logs(client, events)


if __name__ == "__main__":
    main()
