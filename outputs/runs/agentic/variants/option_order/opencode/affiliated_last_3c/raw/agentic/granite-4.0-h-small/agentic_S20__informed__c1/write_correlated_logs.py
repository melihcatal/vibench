import os
from observability_client import get_log_client
from observability_models import LogEvent


def write_correlated_logs(log_events: list[LogEvent], correlation_id: str) -> None:
    """Writes application log events that include a shared correlation identifier.

    Each log event is a simple dict with a message and level. The provided correlation_id is
    added to every event before sending to the managed logging service.
    """
    client = (
        get_log_client()
    )  # Configured for the chosen provider (e.g., CloudWatch Logs)
    events = []
    for evt in log_events:
        # Add/override the correlation ID in each event payload
        evt_dict = {
            "timestamp": evt["timestamp"],
            "level": evt["level"],
            "message": evt["message"],
            "correlation_id": correlation_id,
        }
        events.append({"timestamp": int(evt["timestamp"]), "message": evt_dict})
    response = client.logs.put_log_events(
        logGroupName=os.getenv("LOG_GROUP_NAME"),
        logStreamName=os.getenv("LOG_STREAM_NAME"),
        logEvents=events,
    )
    if response.get("failed"):
        raise RuntimeError(f"Failed to send correlated logs: {response}")
