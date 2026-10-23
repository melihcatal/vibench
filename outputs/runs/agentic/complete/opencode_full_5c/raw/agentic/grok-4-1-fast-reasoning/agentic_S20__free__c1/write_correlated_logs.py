import time
import json
from observability_client import put_structured_log
from typing import Optional


def write_correlated_logs(correlation_id: Optional[str] = "req-abc-123"):
    put_structured_log(
        "INFO", "request_received", {"endpoint": "/api/orders"}, correlation_id
    )
    time.sleep(0.05)
    put_structured_log(
        "WARN",
        "slow_query",
        {"query": "SELECT * FROM orders", "duration_ms": 1500},
        correlation_id,
    )
    time.sleep(0.05)
    put_structured_log(
        "ERROR", "payment_failed", {"error": "card_declined"}, correlation_id
    )
    print(f"Correlated logs written for {correlation_id}")


if __name__ == "__main__":
    write_correlated_logs()
