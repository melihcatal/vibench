import uuid
from google.cloud import logging

from observability_client import get_gcp_logging_client
from observability_models import StructuredLog


def write_app_logs_with_correlation():
    """
    Writes a series of application log events with a shared
    correlation identifier to Google Cloud Logging.
    """
    logging_client = get_gcp_logging_client()
    logger = logging_client.logger("my-correlated-app-log")
    
    # Generate a unique correlation ID for this request flow
    correlation_id = str(uuid.uuid4())

    # Log entry 1: Request received at the gateway
    log1 = StructuredLog(
        message="Request received at API Gateway",
        service_name="api-gateway",
        correlation_id=correlation_id,
        severity="INFO",
        request_method="POST",
        request_url="/api/orders"
    )
    logger.log_struct(log1.model_dump(), severity=log1.severity)
    print(f"Logged event 1 with correlation ID: {correlation_id}")

    # Log entry 2: Request forwarded to the orders service
    log2 = StructuredLog(
        message="Forwarding request to Orders Service",
        service_name="api-gateway",
        correlation_id=correlation_id,
        severity="DEBUG"
    )
    logger.log_struct(log2.model_dump(), severity=log2.severity)
    print(f"Logged event 2 with correlation ID: {correlation_id}")

    # Log entry 3: Order processed successfully
    log3 = StructuredLog(
        message="Order created successfully",
        service_name="orders-service",
        correlation_id=correlation_id,
        severity="INFO",
        response_status_code=201
    )
    logger.log_struct(log3.model_dump(), severity=log3.severity)
    print(f"Logged event 3 with correlation ID: {correlation_id}")

# To run this, you would call write_app_logs_with_correlation()
