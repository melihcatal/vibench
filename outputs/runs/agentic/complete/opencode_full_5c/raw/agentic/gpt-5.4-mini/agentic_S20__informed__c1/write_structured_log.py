from observability_client import client_from_env
from observability_models import LogEvent


def write_structured_log(
    message: str, severity: str = "INFO", service: str = "checkout"
):
    client = client_from_env()
    event = LogEvent(message=message, severity=severity, service=service)
    return client.put_event(event)
