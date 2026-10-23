
import os
import uuid
from observability_client import get_gcp_logging_client
from observability_models import StructuredLog

def write_correlated_log_entries(log_name: str):
    """
    Writes a series of correlated log entries to Google Cloud Logging
    using a shared trace ID.
    """
    logging_client = get_gcp_logging_client()
    logger = logging_client.logger(log_name)

    # Generate a unique correlation ID for this request
    correlation_id = str(uuid.uuid4())

    # In Google Cloud Logging, the 'trace' field is used for correlation
    # projects/[PROJECT_ID]/traces/[TRACE_ID]
    project_id = os.getenv("GCP_PROJECT_ID")
    trace = f"projects/{project_id}/traces/{correlation_id}"

    # Log the start of the request
    start_log = StructuredLog(
        message="Request received to process order.",
        severity="INFO",
        request_id=correlation_id,
        service_context="order-service",
    )
    logger.log_json(start_log.to_dict(), resource=None, trace=trace)
    print(f"Logged start of request {correlation_id}")

    # Log a dependency call
    dep_log = StructuredLog(
        message="Calling payment gateway.",
        severity="DEBUG",
        request_id=correlation_id,
        service_context="order-service",
        custom_dimensions={"gateway": "stripe"}
    )
    logger.log_json(dep_log.to_dict(), resource=None, trace=trace)
    print(f"Logged dependency call for request {correlation_id}")

    # Log the completion of the request
    end_log = StructuredLog(
        message="Order processed successfully.",
        severity="INFO",
        request_id=correlation_id,
        service_context="order-service",
    )
    logger.log_json(end_log.to_dict(), resource=None, trace=trace)
    print(f"Logged completion of request {correlation_id}")


if __name__ == '__main__':
    LOG_NAME = os.getenv("GCP_LOG_NAME", "my-correlated-log")
    write_correlated_log_entries(LOG_NAME)
