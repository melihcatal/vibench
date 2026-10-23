import time
import json
from observability_client import CloudWatchLogsClient
from observability_models import normalize_log_event

def write_correlated_logs(log_group_name, log_stream_name, correlation_id, events, region_name=None):
    client = CloudWatchLogsClient(region_name=region_name)
    log_events = []
    for event_data in events:
        payload = {
            "timestamp_ms": int(time.time() * 1000),
            "event": {
                "correlation_id": correlation_id,
                **event_data,
            }
        }
        normalized_event = normalize_log_event(payload)
        log_events.append({
            "timestamp": normalized_event["timestamp"],
            "message": normalized_event["message"],
        })
    
    response = client.put_log_events(log_group_name, log_stream_name, log_events)
    return {"submitted": True, "response": response}
