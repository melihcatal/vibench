import os
from observability_client import ManagedLogClient


def write_correlated_logs(log_entries: list, correlation_id: str) -> list:
    """Writes application log events that include a shared request/correlation identifier.

    Args:
        log_entries (list): List of dict log payloads.
        correlation_id (str): Common ID linking the logs together.

    Returns:
        list: Responses from the logging service for each entry.
    """
    client = ManagedLogClient()
    responses = []
    for entry in log_entries:
        # Enrich each log with the correlation identifier
        enriched = entry.copy()
        enriched["correlation_id"] = correlation_id
        resp = client.write_log(
            log_name="app-operations",
            resource_type="global",
            severity="info",
            payload=os.environ.get("LOG_FORMAT", "json").lower() + f": {entry}",
        )
        responses.append(resp)
    return responses
