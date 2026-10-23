import os
import uuid
from observability_client import get_logging_client
from observability_models import LogEntry
from google.cloud.logging.resource import Resource


def write_correlated_logs(
    log_entries: list[LogEntry],
    correlation_id: str,
    log_name: str = "my-correlated-log",
):
    """Writes multiple log entries with a shared correlation ID.

    The correlation ID is added to the 'trace' field for GCP Trace correlation.
    """
    logging_client = get_logging_client()
    logger = logging_client.logger(log_name)

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        # Fallback to client's project if not in env
        project_id = logging_client.project

    trace_id = f"projects/{project_id}/traces/{correlation_id}"

    for entry in log_entries:
        logger.log_json(entry, trace=trace_id)
        print(f"Wrote log with correlation ID {correlation_id}: {entry['message']}")


if __name__ == "__main__":
    # Example Usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables.

    request_id = str(uuid.uuid4())

    logs = [
        {"message": "Received request to process order.", "order_id": "order_abc"},
        {
            "message": "Validating payment information.",
            "order_id": "order_abc",
            "payment_gateway": "stripe",
        },
        {
            "message": "Order processing complete.",
            "order_id": "order_abc",
            "status": "success",
        },
    ]

    write_correlated_logs(logs, request_id)
