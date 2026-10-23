import json
import os
from observability_client import get_ingestion_client, get_correlation_id


def write_correlated_logs(
    service_name: str, events: list[dict], request_id: str = None
):
    """Writes application log events that include a shared request/correlation identifier.

    Each event in `events` should be a dict that will be sent as a structured log.
    The provided `request_id` (or the one from the execution context) is attached to all events.
    """
    client = get_ingestion_client()
    correlation_id = request_id or get_correlation_id()
    for event in events:
        event["correlation_id"] = correlation_id
        client.log(event)
