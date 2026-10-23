from observability_client import AzureMonitorClient
from observability_models import LogEvent
from datetime import datetime
import uuid
import json

def write_correlated_logs(correlation_id: str, application_name: str, messages: list[dict]):
    client = AzureMonitorClient()
    log_entries = []
    for msg_data in messages:
        message = msg_data.get("message")
        severity = msg_data.get("severity", "Informational")
        properties = msg_data.get("properties", {})
        
        # Add correlation_id and application_name to properties
        properties["correlation_id"] = correlation_id
        properties["application_name"] = application_name

        log_event = LogEvent(
            message=message,
            severity=severity,
            properties=properties,
            timestamp=datetime.utcnow()
        )
        log_entries.append(json.loads(log_event.to_json()))
    
    client.ingest_logs(log_entries, log_stream_name="Custom-MyApplicationLogs")

if __name__ == "__main__":
    # Example usage
    request_id = str(uuid.uuid4())
    print(f"Using correlation ID: {request_id}")

    log_messages = [
        {
            "message": "Request received for user profile.",
            "severity": "Informational",
            "properties": {"user_id": "user_123", "endpoint": "/profile"}
        },
        {
            "message": "Fetching data from database.",
            "severity": "Informational",
            "properties": {"db_query": "SELECT * FROM users WHERE id='user_123'"}
        },
        {
            "message": "Successfully retrieved user profile.",
            "severity": "Informational",
            "properties": {"response_time_ms": 50}
        }
    ]

    write_correlated_logs(request_id, "UserManagementService", log_messages)

    error_request_id = str(uuid.uuid4())
    print(f"Using error correlation ID: {error_request_id}")
    error_messages = [
        {
            "message": "Initiating transaction.",
            "severity": "Informational",
            "properties": {"transaction_id": "txn_001"}
        },
        {
            "message": "Payment gateway timed out.",
            "severity": "Error",
            "properties": {"payment_gateway": "stripe", "timeout_ms": 5000}
        },
        {
            "message": "Transaction failed, rolling back.",
            "severity": "Critical",
            "properties": {"transaction_id": "txn_001", "rollback_status": "complete"}
        }
    ]
    write_correlated_logs(error_request_id, "PaymentService", error_messages)
