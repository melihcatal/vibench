import json
import time
import os

from observability_client import ObservabilityClient
from observability_models import LogEvent

def write_correlated_logs(log_events: list[LogEvent], log_group: str, correlation_id: str, config=None):
    config = config or {}
    client = ObservabilityClient(region_name=config.get("region"))
    
    # Group log events by log stream name as CloudWatch Logs expects events per stream
    events_by_stream = {}
    for event in log_events:
        if event.log_stream_name not in events_by_stream:
            events_by_stream[event.log_stream_name] = []
        events_by_stream[event.log_stream_name].append({
            "timestamp": int(event.timestamp_ms),
            "message": json.dumps({"correlation_id": correlation_id, **json.loads(event.message)}),
        })
    
    results = []
    for stream_name, events in events_by_stream.items():
        response = client.put_log_events(
            log_group_name=log_group,
            log_stream_name=stream_name,
            log_events=events,
        )
        results.append(response)
        
    return results
