from google.cloud import logging
from google.cloud.logging.resource import Resource
import os
import uuid
import time


def write_correlated_logs():
    """Writes several log entries with a shared correlation ID."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    client = logging.Client(project=project_id)
    log_name = "correlated-log-test"
    logger = client.logger(log_name)

    res = Resource(type="global", labels={})

    correlation_id = str(uuid.uuid4())
    # The trace field in Google Cloud Logging is used for correlation.
    # Format: projects/[PROJECT_ID]/traces/[TRACE_ID]
    trace_id = f"projects/{project_id}/traces/{correlation_id}"

    logger.log_text(
        "Request started.",
        resource=res,
        severity="INFO",
        trace=trace_id,
    )

    time.sleep(0.1)

    # Adding correlation_id also to json_payload for easy querying
    json_payload_auth = {
        "message": "User authentication successful.",
        "user_id": "user_abc",
        "correlation_id": correlation_id,
    }
    logger.log_json(
        json_payload_auth,
        resource=res,
        severity="INFO",
        trace=trace_id,
    )

    time.sleep(0.1)

    json_payload_db = {
        "message": "Database query executed.",
        "db_query_time_ms": 150,
        "correlation_id": correlation_id,
    }
    logger.log_json(
        json_payload_db,
        resource=res,
        severity="DEBUG",
        trace=trace_id,
    )

    time.sleep(0.1)

    logger.log_text(
        "Request finished.",
        resource=res,
        severity="INFO",
        trace=trace_id,
    )


if __name__ == "__main__":
    write_correlated_logs()
