# Same-scenario implementation
import uuid
from observability_client import get_logging_client


def write_correlated_logs(correlation_id, log_entries):
    """Writes application log events that include a shared correlation identifier.

    Uses Loggly (example provider). Each log entry is augmented with the
    supplied correlation_id, then sent to the managed logging service.
    """
    client = get_logging_client()
    for entry in log_entries:
        enriched = {**entry, "correlation_id": correlation_id}
        client.send_log(json.dumps(enriched))
