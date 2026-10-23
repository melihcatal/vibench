from observability_client import ObservabilityClient
from observability_models import LogEvent
from typing import List


def write_correlated_logs(messages: List[str], correlation_id: str) -> dict:
    client = ObservabilityClient()
    logs = []
    for message in messages:
        event = LogEvent(message=message, correlation_id=correlation_id, level="info")
        dd_log = {
            "message": message,
            "service": event.service,
            "status": event.level,
            "env": event.env,
            "correlation_id": correlation_id,
        }
        logs.append(dd_log)
    response = client.submit_logs(logs)
    return {"status": response.status_code, "count": len(logs)}
