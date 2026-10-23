import os
from observability_client import write_log
from observability_models import LogEvent

# Datadog provider
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")

def write_structured_log(message: str, severity: str = "INFO", service: str = "myapp", env: str = "prod", **kwargs) -> bool:
    """
    Writes a structured JSON log event to Datadog.
    """
    event = LogEvent(
        message=message,
        severity=severity,
        service=service,
        env=env,
        **kwargs
    )
    return write_log(event)