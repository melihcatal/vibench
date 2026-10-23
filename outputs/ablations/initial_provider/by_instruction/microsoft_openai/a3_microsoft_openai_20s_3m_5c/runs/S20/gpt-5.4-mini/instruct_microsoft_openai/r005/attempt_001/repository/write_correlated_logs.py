from observability_client import write_log
from observability_models import StructuredLogEvent


def main() -> list:
    correlation_id = "req_abc123"
    return [write_log(StructuredLogEvent(message="request started", severity="info", service="api", correlation_id=correlation_id, fields={"path": "/v1/orders"})), write_log(StructuredLogEvent(message="request completed", severity="info", service="api", correlation_id=correlation_id, fields={"status": 200}))]
