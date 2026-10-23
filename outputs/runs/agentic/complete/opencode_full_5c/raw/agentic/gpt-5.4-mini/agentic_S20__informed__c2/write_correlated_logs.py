from observability_client import DatadogObservabilityClient
from observability_models import LogEvent


def write_correlated_logs() -> dict:
    client = DatadogObservabilityClient()
    request_id = "req-7c3b3c90"
    events = [
        LogEvent.create(
            "api-gateway",
            "info",
            "request accepted",
            {"request_id": request_id, "path": "/v1/payments"},
        ),
        LogEvent.create(
            "payments-worker",
            "info",
            "payment processed",
            {"request_id": request_id, "payment_id": "pay_42"},
        ),
    ]
    return {"results": [client.write_log(event) for event in events]}
