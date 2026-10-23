import time
import json
from typing import Dict, Any, List
from observability_client import ObservabilityClient
from observability_models import LogEvent

def write_correlated_logs(log_group_name: str, log_stream_name: str, correlation_id: str, messages: List[Dict[str, Any]]):
    client = ObservabilityClient()
    log_events_to_send = []

    for msg in messages:
        # Add correlation_id to each message
        msg['correlation_id'] = correlation_id
        timestamp = int(time.time() * 1000)
        log_event = LogEvent(message=msg, timestamp=timestamp, log_stream_name=log_stream_name)
        log_events_to_send.append(log_event.to_aws_cloudwatch_format())

    response = client.put_log_events(
        log_group_name=log_group_name,
        log_stream_name=log_stream_name,
        log_events=log_events_to_send
    )
    return response
