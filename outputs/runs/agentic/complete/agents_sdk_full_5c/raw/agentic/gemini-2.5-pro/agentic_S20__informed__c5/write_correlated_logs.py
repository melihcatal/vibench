import uuid
from observability_client import get_logger

def write_application_logs_with_correlation():
    """
    Writes multiple application logs with a shared correlation ID
    to Google Cloud Logging.
    """
    logger = get_logger("correlated_log_writer")
    correlation_id = str(uuid.uuid4())

    print(f"Using correlation ID: {correlation_id}")

    # Log the start of a request
    start_payload = {
        "message": "Processing started for user request.",
        "service": "api-gateway",
        "correlation_id": correlation_id,
        "endpoint": "/api/v1/process",
        "method": "POST",
    }
    logger.log_struct(start_payload, severity="INFO")
    print("Logged request start.")

    # Log a warning during processing
    warning_payload = {
        "message": "Upstream service latency detected.",
        "service": "data-processor",
        "correlation_id": correlation_id,
        "upstream_service": "user-profile-service",
        "latency_ms": 1500,
    }
    logger.log_struct(warning_payload, severity="WARNING")
    print("Logged processing warning.")

    # Log the successful completion of the request
    end_payload = {
        "message": "Successfully processed user request.",
        "service": "api-gateway",
        "correlation_id": correlation_id,
        "status_code": 200,
    }
    logger.log_struct(end_payload, severity="INFO")
    print("Logged request completion.")


if __name__ == '__main__':
    write_application_logs_with_correlation()
