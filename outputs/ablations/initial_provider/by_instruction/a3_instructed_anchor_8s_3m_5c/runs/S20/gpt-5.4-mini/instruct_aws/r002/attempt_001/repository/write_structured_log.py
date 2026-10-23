from observability_client import ObservabilityClient
from observability_models import LogEvent


def write_structured_log(message, severity="INFO", service="app", **fields):
    client = ObservabilityClient()
    event = LogEvent(message=message, severity=severity, service=service, fields=fields)
    return client.write_log_event(event)
