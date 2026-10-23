import datetime
import uuid
from observability_client import ObservabilityClient
from observability_models import CorrelatedLogEvent

def write_correlated_logs(correlation_id: str, service_name: str, events: list[dict]):
    client = ObservabilityClient()
    
    log_events = []
    for event in events:
        log_event = CorrelatedLogEvent(
            message=event["message"],
            severity=event.get("severity", "Informational"),
            service_name=service_name,
            correlation_id=correlation_id,
            event_timestamp=datetime.datetime.utcnow().isoformat(),
            **event.get("data", {})
        )
        log_events.append(log_event.to_json())
    
    log_type = "MyCorrelatedApplicationLogs"
    
    try:
        client.post_log_event(log_type, log_events)
    except Exception as e:
        print(f"Error writing correlated logs: {e}")