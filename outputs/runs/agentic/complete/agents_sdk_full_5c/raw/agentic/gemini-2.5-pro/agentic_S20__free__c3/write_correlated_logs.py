import uuid
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem

from observability_client import get_datadog_client
from observability_models import StructuredLog

def send_correlated_logs():
    """
    Sends multiple log events with a shared correlation ID to Datadog.
    """
    logs_api = get_datadog_client()
    correlation_id = str(uuid.uuid4())

    log_events = [
        StructuredLog(
            message="Starting transaction for user 'testuser'.",
            service="api-gateway",
            level="INFO",
            extra_attributes={"correlation_id": correlation_id, "user": "testuser"}
        ),
        StructuredLog(
            message="Authenticating user 'testuser'.",
            service="auth-service",
            level="INFO",
            extra_attributes={"correlation_id": correlation_id}
        ),
        StructuredLog(
            message="User 'testuser' authenticated successfully.",
            service="auth-service",
            level="INFO",
            extra_attributes={"correlation_id": correlation_id}
        ),
        StructuredLog(
            message="Failed to process payment for user 'testuser'.",
            service="payment-service",
            level="ERROR",
            extra_attributes={"correlation_id": correlation_id, "error_code": "PMT-5001"}
        )
    ]

    log_payloads = [HTTPLogItem(**event.to_datadog_payload()) for event in log_events]

    try:
        logs_api.submit_log(HTTPLog(log_payloads))
        print(f"Successfully sent {len(log_payloads)} correlated logs to Datadog.")
    except Exception as e:
        print(f"Error sending logs to Datadog: {e}")
