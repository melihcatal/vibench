from observability_client import AzureMonitorClient
from observability_models import LogEvent
from datetime import datetime

def write_structured_log(message: str, severity: str, event_properties: dict):
    client = AzureMonitorClient()
    log_event = LogEvent(
        message=message,
        severity=severity,
        properties=event_properties,
        timestamp=datetime.utcnow()
    )
    
    # Azure Monitor expects a list of dictionaries for ingestion
    client.ingest_logs([json.loads(log_event.to_json())], log_stream_name="Custom-MyApplicationLogs")

if __name__ == "__main__":
    import json
    # Example usage
    structured_log_properties = {
        "application": "web_app",
        "component": "user_auth",
        "user_id": "user123",
        "ip_address": "192.168.1.100",
        "request_id": "req_abc123"
    }
    write_structured_log(
        message="User login successful.",
        severity="Informational",
        event_properties=structured_log_properties
    )

    error_log_properties = {
        "application": "api_service",
        "component": "data_processor",
        "error_code": 500,
        "exception_type": "NullPointerException",
        "request_id": "req_xyz456"
    }
    write_structured_log(
        message="Failed to process data due to an unexpected error.",
        severity="Error",
        event_properties=error_log_properties
    )
