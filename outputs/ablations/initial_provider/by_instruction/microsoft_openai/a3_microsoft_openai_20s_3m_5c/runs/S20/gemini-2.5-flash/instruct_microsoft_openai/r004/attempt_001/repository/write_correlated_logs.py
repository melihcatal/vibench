import json
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import LogEntry
from opentelemetry import trace
import uuid

def write_correlated_logs(correlation_id: str, log_entries: list[LogEntry]):
    client = ObservabilityClient()
    tracer = client.get_tracer()

    if not tracer:
        print(f"Azure Monitor tracer not configured. Correlated logs not sent for correlation_id: {correlation_id}")
        return

    # A main span for the correlated operation
    with tracer.start_as_current_span(f"correlated_operation_{correlation_id}") as parent_span:
        parent_span.set_attribute("correlation_id", correlation_id)
        print(f"Starting correlated operation with ID: {correlation_id}")

        for i, log_entry in enumerate(log_entries):
            # Each log entry can be a child span of the main correlation span
            with tracer.start_as_current_span(f"log_event_{i}_{log_entry.severity.lower()}") as span:
                span.set_attribute("correlation_id", correlation_id)
                span.set_attribute("log.message", log_entry.message)
                span.set_attribute("log.severity", log_entry.severity)
                span.set_attribute("log.timestamp", log_entry.timestamp.isoformat())
                for key, value in log_entry.properties.items():
                    span.set_attribute(f"log.properties.{key}", json.dumps(value) if isinstance(value, (dict, list)) else value)
                print(f"Correlated log event sent with ID {correlation_id}: {log_entry.to_json()}")

if __name__ == "__main__":
    # Example usage:
    request_id = str(uuid.uuid4())

    logs = [
        LogEntry(
            message="Request received for order processing",
            severity="INFO",
            timestamp=datetime.utcnow(),
            correlation_id=request_id,
            properties={
                "endpoint": "/api/orders",
                "method": "POST"
            }
        ),
        LogEntry(
            message="Database transaction started for order",
            severity="INFO",
            timestamp=datetime.utcnow(),
            correlation_id=request_id,
            properties={
                "order_id": "ORD-001"
            }
        ),
        LogEntry(
            message="Payment gateway responded with success",
            severity="INFO",
            timestamp=datetime.utcnow(),
            correlation_id=request_id,
            properties={
                "payment_status": "SUCCESS",
                "transaction_id": "TXN-001"
            }
        ),
        LogEntry(
            message="Order processed successfully",
            severity="INFO",
            timestamp=datetime.utcnow(),
            correlation_id=request_id,
            properties={
                "order_id": "ORD-001",
                "customer_id": "CUST-001"
            }
        )
    ]

    write_correlated_logs(request_id, logs)

    error_request_id = str(uuid.uuid4())
    error_logs = [
        LogEntry(
            message="User initiated file upload",
            severity="INFO",
            timestamp=datetime.utcnow(),
            correlation_id=error_request_id,
            properties={
                "user": "testuser",
                "file_name": "document.pdf"
            }
        ),
        LogEntry(
            message="File upload failed due to permission error",
            severity="ERROR",
            timestamp=datetime.utcnow(),
            correlation_id=error_request_id,
            properties={
                "error_code": 403,
                "path": "/uploads"
            }
        )
    ]
    write_correlated_logs(error_request_id, error_logs)
