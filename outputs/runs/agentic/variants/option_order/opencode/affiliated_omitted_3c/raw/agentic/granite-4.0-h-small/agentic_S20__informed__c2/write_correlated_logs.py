import json
import os
from observability_client import get_log_client


def write_correlated_logs(logs: list[dict], correlation_id: str):
    """Write application log events that include a shared correlation identifier.

    Expect a list of log dicts; each entry is enriched with the given
    `correlation_id` before being sent to the managed logging service.
    """
    enriched_logs = []
    client = get_log_client()
    for entry in logs:
        enriched = entry.copy()
        enriched["correlation_id"] = correlation_id
        enriched_logs.append(enriched)
    # Provider‑specific payload sending (e.g., bulk endpoint or synchronous send)
    client.send_logs(json.dumps(enriched_logs))
