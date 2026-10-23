import uuid
from observability_client import get_logging_client

LOG_NAME = "my-application-logs"


def write_correlated_logs(correlation_id: str):
    """
    Writes a series of application log events that share a correlation ID.
    This ID is added to the 'trace' field for correlation in Google Cloud Logging.

    Args:
        correlation_id (str): The shared identifier for the request or transaction.
    """
    logging_client = get_logging_client()
    logger = logging_client.logger(LOG_NAME)

    project_id = logging_client.project
    trace_id = f"projects/{project_id}/traces/{correlation_id}"

    # Log the start of an operation
    log_1 = {
        "message": "Processing started for request.",
        "service": "api-gateway",
        "correlation_id": correlation_id,
    }
    logger.log_json(log_1, severity="INFO", trace=trace_id)
    print(f"Logged: {log_1['message']}")

    # Log a downstream operation
    log_2 = {
        "message": "Fetching user data from database.",
        "service": "user-service",
        "correlation_id": correlation_id,
    }
    logger.log_json(log_2, severity="INFO", trace=trace_id)
    print(f"Logged: {log_2['message']}")

    # Log the completion of the operation
    log_3 = {
        "message": "Processing finished successfully.",
        "service": "api-gateway",
        "correlation_id": correlation_id,
    }
    logger.log_json(log_3, severity="INFO", trace=trace_id)
    print(f"Logged: {log_3['message']}")


# Example of how this might be called (not executed):
# if __name__ == '__main__':
#     request_id = str(uuid.uuid4())
#     write_correlated_logs(request_id)
