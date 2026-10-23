import logging
import os
from datetime import datetime
from observability_client import get_azure_log_analytics_client
from observability_models import StructuredLogEvent

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Get Azure Log Analytics handler
handler = get_azure_log_analytics_client()
if handler:
    logger.addHandler(handler)

def write_structured_log(message: str, severity: str, **kwargs):
    """Writes a structured JSON log event to Azure Log Analytics."""
    timestamp = datetime.utcnow().isoformat() + "Z"
    log_event = StructuredLogEvent(message, severity, timestamp, **kwargs)
    
    # The AzureLogHandler expects a log record. We can pass our structured log
    # as an 'extra' dictionary, and it will be included in the customDimensions
    # in Azure Monitor.
    try:
        logger.info(message, extra=log_event.properties)
        print(f"Structured log event sent to Azure Monitor: {{log_event.to_json()}}")
    except Exception as e:
        print(f"Error sending log to Azure Monitor: {e}")

if __name__ == "__main__":
    # Example usage
    os.environ["AZURE_MONITOR_CONNECTION_STRING"] = "InstrumentationKey=YOUR_INSTRUMENTATION_KEY"
    # Replace with your actual connection string for testing

    write_structured_log(
        message="User login successful",
        severity="INFO",
        user_id="user123",
        ip_address="192.168.1.1",
        service="auth_service"
    )

    write_structured_log(
        message="Failed to process payment",
        severity="ERROR",
        user_id="user456",
        transaction_id="txn789",
        error_code="PAYMENT_GATEWAY_TIMEOUT"
    )
