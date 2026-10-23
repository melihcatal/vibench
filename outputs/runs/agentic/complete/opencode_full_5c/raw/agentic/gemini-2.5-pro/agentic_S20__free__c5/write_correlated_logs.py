import os
import uuid
import time
from typing import List
from observability_client import get_log_writer_client
from observability_models import StructuredLog


def write_correlated_log_entries(log_name: str, logs: List[StructuredLog]):
    """Writes a batch of correlated log entries to Google Cloud Logging."""
    client = get_log_writer_client()
    logger = client.logger(log_name)

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    correlation_id = str(uuid.uuid4())

    with client.batch() as batch:
        for log in logs:
            log.trace_id = f"projects/{project_id}/traces/{correlation_id}"
            payload = log.model_dump(exclude_none=True)
            batch.log_struct(payload, severity=log.severity)

    print(
        f"Wrote {len(logs)} correlated logs to {log_name} with trace_id containing '{correlation_id}'"
    )


if __name__ == "__main__":
    # Example Usage:
    # Set the GOOGLE_CLOUD_PROJECT environment variable
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        request_id = str(uuid.uuid4())
        log_entries = [
            StructuredLog(
                message="Received request to process order.",
                severity="INFO",
                context={"order_id": "order-abcde", "request_id": request_id},
            ),
            StructuredLog(
                message="Fetching user details.",
                severity="DEBUG",
                context={"user_id": "user-12345", "request_id": request_id},
            ),
            StructuredLog(
                message="Payment processing failed.",
                severity="ERROR",
                context={"reason": "Insufficient funds", "request_id": request_id},
            ),
        ]
        write_correlated_log_entries("my-correlated-log", log_entries)
