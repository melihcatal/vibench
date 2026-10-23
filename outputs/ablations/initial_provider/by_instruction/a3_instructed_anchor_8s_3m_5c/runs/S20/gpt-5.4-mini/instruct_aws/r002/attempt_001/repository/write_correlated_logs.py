from observability_client import ObservabilityClient
from observability_models import LogEvent


def write_correlated_logs(message, request_id, correlation_id, severity="INFO", service="app", **fields):
    client = ObservabilityClient()
    event = LogEvent(
        message=message,
        severity=severity,
        service=service,
        request_id=request_id,
        correlation_id=correlation_id,
        fields=fields,
    )
    return client.write_log_event(event)
