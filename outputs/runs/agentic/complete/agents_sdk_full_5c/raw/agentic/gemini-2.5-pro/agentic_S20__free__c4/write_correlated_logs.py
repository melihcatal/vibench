import uuid
from observability_client import get_gcp_logging_client

def write_correlated_log_entries(log_name: str = "my-correlated-log"):
    """
    Writes multiple log entries with a shared correlation ID to Google Cloud Logging.

    Args:
        log_name: The name of the log to write to.
    """
    logging_client = get_gcp_logging_client()
    logger = logging_client.logger(log_name)

    # Generate a unique correlation ID for this request
    correlation_id = str(uuid.uuid4())

    # Log the start of the request
    logger.log_struct(
        {
            "message": "Processing started for new user request.",
            "correlation_id": correlation_id,
            "stage": "begin_processing",
        },
        severity="INFO",
    )

    # Log a midway point
    logger.log_struct(
        {
            "message": "User data validated.",
            "correlation_id": correlation_id,
            "stage": "validation_complete",
            "validation_time_ms": 150,
        },
        severity="INFO",
    )

    # Log the completion of the request
    logger.log_struct(
        {
            "message": "Successfully processed new user request.",
            "correlation_id": correlation_id,
            "stage": "end_processing",
        },
        severity="INFO",
    )

    print(f"Wrote 3 correlated log entries with ID: {correlation_id}")


if __name__ == "__main__":
    write_correlated_log_entries()
