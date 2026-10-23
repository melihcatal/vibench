import uuid
from datetime import datetime
from observability_client import get_logging_client
from observability_models import StructuredLogEvent


def write_correlated_logs(request_id: str = None) -> list:
    """Write application logs with a shared correlation ID to Datadog."""
    client = get_logging_client()
    correlation_id = request_id or str(uuid.uuid4())
    
    logs = [
        StructuredLogEvent(
            timestamp=datetime.utcnow().isoformat(),
            severity="INFO",
            message="Request started",
            attributes={
                "correlation_id": correlation_id,
                "stage": "start"
            }
        ).dict(),
        StructuredLogEvent(
            timestamp=datetime.utcnow().isoformat(),
            severity="INFO",
            message="Request processed",
            attributes={
                "correlation_id": correlation_id,
                "stage": "process"
            }
        ).dict()
    ]
    
    responses = client.submit_logs(logs)
    return [resp.get("log_id") for resp in responses]