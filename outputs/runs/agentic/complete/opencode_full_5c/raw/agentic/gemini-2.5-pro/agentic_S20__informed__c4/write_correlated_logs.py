import os
import uuid
from observability_client import get_logging_client


def write_correlated_logs(logger_name: str, request_id: str = None):
    """
    Writes a series of application log events with a shared correlation ID.

    Args:
        logger_name: The name of the logger.
        request_id: A specific request ID to use for correlation.
                    If None, a new UUID will be generated.
    """
    client = get_logging_client()
    logger = client.logger(logger_name)

    correlation_id = request_id or str(uuid.uuid4())

    log_entries = [
        {"message": "Received request to process user data.", "step": "start"},
        {"message": "Fetching user profile from database.", "step": "db_query"},
        {"message": "Performing data transformation.", "step": "transform"},
        {"message": "Data processing complete.", "step": "finish"},
    ]

    with client.batch() as batch:
        for entry in log_entries:
            payload = {"correlation_id": correlation_id, **entry}
            batch.log_json(payload)

    print(
        f"Successfully wrote 4 correlated logs to '{logger_name}' with ID: {correlation_id}"
    )


if __name__ == "__main__":
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        write_correlated_logs("correlated_log_writer")
    else:
        print("GOOGLE_APPLICATION_CREDENTIALS not set. Skipping example run.")
