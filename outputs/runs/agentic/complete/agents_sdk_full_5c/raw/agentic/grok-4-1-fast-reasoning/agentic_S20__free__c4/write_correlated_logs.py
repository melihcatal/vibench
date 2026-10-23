import os
from typing import List, Dict
from observability_client import write_logs
from observability_models import LogEvent

# Datadog provider
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")

def write_correlated_logs(events_data: List[Dict], correlation_id: str) -> bool:
    """
    Writes application log events that include a shared request or correlation identifier to Datadog.
    """
    events = []
    for data in events_data:
        event = LogEvent(
            message=data["message"],
            severity=data.get("severity", "INFO"),
            service=data.get("service", "myapp"),
            env=data.get("env", "prod"),
            trace_id=correlation_id,
            **{k: v for k, v in data.items() if k not in ["message", "severity", "service", "env"]}
        )
        events.append(event)
    return write_logs(events)