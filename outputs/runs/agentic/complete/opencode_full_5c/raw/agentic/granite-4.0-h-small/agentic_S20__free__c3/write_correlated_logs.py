import json
from datetime import datetime, timedelta


def write_correlated_logs(service: str, events: list[dict], correlation_id: str):
    """Write multiple structured log events that share a common correlation identifier.
    Each event must be a dict with at least 'message' and 'severity'.
    """
    payload = {"service": service, "correlation_id": correlation_id, "logs": []}
    for evt in events:
        log = {
            "message": evt.get("message"),
            "severity": evt.get("severity"),
            "timestamp": evt.get(
                "timestamp", int(datetime.utcnow().timestamp() * 1000)
            ),
        }
        payload["logs"].append(log)
    # In production, POST payload to Datadog Logs API
    print(f"[WRITE_CORRELATED] Payload (JSON): {json.dumps(payload, indent=2)}")


# Example (not executed)
# write_correlated_logs(
#     service="order-service",
#     events=[
#         {"message": "Order created", "severity": "info"},
#         {"message": "Payment processed", "severity": "info"}
#     ],
#     correlation_id="req-9876")
