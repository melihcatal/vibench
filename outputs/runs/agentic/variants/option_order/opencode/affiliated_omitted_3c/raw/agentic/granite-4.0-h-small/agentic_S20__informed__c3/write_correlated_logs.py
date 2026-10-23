import json
import os
from observability_client import get_log_client


def write_correlated_logs(events: list[dict], correlation_id: str) -> None:
    """Writes a batch of log events, each enriched with a shared request/correlation identifier.

    Uses Datadog Logs API (REST) with the requests library.
    """
    client = get_log_client()  # requests.Session configured for Datadog
    payload = [
        {"ddsource": "app", "ddtags": f"request_id:{correlation_id}", **event}
        for event in events
    ]
    resp = client.post(
        url="https://http-intake.logs.datadoghq.com/v1/input",
        headers={
            "DD-API-KEY": os.getenv("DD_API_KEY"),
            "Content-Type": "application/json",
        },
        json=payload,
    )
    resp.raise_for_status()
