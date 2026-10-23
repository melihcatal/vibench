import time
import json
from typing import Dict, Any
from observability_client import ObservabilityClient
from observability_models import LogEvent

def write_structured_log(log_group_name: str, log_stream_name: str, message: Dict[str, Any]):
    client = ObservabilityClient()
    timestamp = int(time.time() * 1000) # Milliseconds

    log_event = LogEvent(message=message, timestamp=timestamp, log_stream_name=log_stream_name)
    aws_log_event = log_event.to_aws_cloudwatch_format()

    response = client.put_log_events(
        log_group_name=log_group_name,
        log_stream_name=log_stream_name,
        log_events=[aws_log_event]
    )
    return response
