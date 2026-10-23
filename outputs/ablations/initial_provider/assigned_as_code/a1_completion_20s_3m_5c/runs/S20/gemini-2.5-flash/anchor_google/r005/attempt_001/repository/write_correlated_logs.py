from observability_client import ObservabilityClient
from datetime import datetime
import uuid

def write_correlated_logs(project_id: str, log_name: str, correlation_id: str = None):
    client = ObservabilityClient(project_id, log_name)

    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    log_event_1 = {
        "event_type": "order_placed",
        "order_id": "12345",
        "user_id": "user-abc",
        "correlationId": correlation_id,
        "timestamp": datetime.now().isoformat()
    }
    client.write_log_entry(log_event_1, severity="INFO")

    log_event_2 = {
        "event_type": "payment_processed",
        "order_id": "12345",
        "payment_status": "success",
        "correlationId": correlation_id,
        "timestamp": datetime.now().isoformat()
    }
    client.write_log_entry(log_event_2, severity="INFO")

    log_event_3 = {
        "event_type": "shipping_initiated",
        "order_id": "12345",
        "shipping_provider": "fedex",
        "correlationId": correlation_id,
        "timestamp": datetime.now().isoformat()
    }
    client.write_log_entry(log_event_3, severity="INFO")

    return {"correlation_id": correlation_id, "submitted_count": 3}

