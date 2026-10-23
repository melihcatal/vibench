import uuid
import os
from observability_client import logging_client, get_gcp_project_id
from observability_models import CorrelatedLog

def write_app_logs_with_correlation(correlation_id: str):
    """
    Writes a series of application logs sharing a correlation ID.
    In Google Cloud Logging, this is achieved using the `trace` field.
    """
    if not logging_client:
        print("Logging client not available. Skipping log write.")
        return

    project_id = get_gcp_project_id()
    # Format for Google Cloud Trace correlation
    trace_identifier = f"projects/{project_id}/traces/{correlation_id}"

    logs = [
        CorrelatedLog(
            message="Request received at gateway.",
            service_name="api-gateway",
            correlation_id=correlation_id,
            severity="INFO",
        ),
        CorrelatedLog(
            message="Authenticated user and forwarding to user-service.",
            service_name="auth-service",
            correlation_id=correlation_id,
            severity="DEBUG",
            details={"user": "user-123"},
        ),
        CorrelatedLog(
            message="User profile retrieved successfully.",
            service_name="user-service",
            correlation_id=correlation_id,
            severity="INFO",
            details={"lookup_time_ms": 55},
        ),
        CorrelatedLog(
            message="Failed to connect to billing database.",
            service_name="billing-service",
            correlation_id=correlation_id,
            severity="ERROR",
            details={"db_host": "10.0.1.23"},
        ),
    ]

    logger = logging_client.get_logger("correlated_app_logger")

    for log in logs:
        payload = {
            "message": log.message,
            "service": log.service_name,
            "correlation_id": log.correlation_id,
            "details": log.details,
        }
        logger.log_struct(
            payload, severity=log.severity, trace=trace_identifier
        )
        print(f"Logged from '{log.service_name}' with correlation ID: {correlation_id}")

    print(f"\nWrote {len(logs)} correlated logs with trace ID '{trace_identifier}'.")


if __name__ == "__main__":
    request_correlation_id = str(uuid.uuid4())
    print(f"Starting process with new Correlation ID: {request_correlation_id}")
    try:
        write_app_logs_with_correlation(request_correlation_id)
    except Exception as e:
        print(f"An error occurred: {e}")
