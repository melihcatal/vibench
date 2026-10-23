import json
import time
from typing import Optional, Dict, Any

from observability_client import (
    get_client,
    LOG_GROUP_NAME,
    LOG_STREAM_NAME,
    ensure_resources,
    get_upload_sequence_token,
)
from observability_models import create_structured_log_event


def write_structured_log(
    message: str,
    level: str = "INFO",
    correlation_id: Optional[str] = None,
    **extra_fields,
):
    ensure_resources()
    log_event_dict = create_structured_log_event(
        message, level=level, correlation_id=correlation_id, **extra_fields
    )
    log_message = json.dumps(log_event_dict)
    timestamp_ms = int(time.time() * 1000)
    events = [{"timestamp": timestamp_ms, "message": log_message}]
    client = get_client()
    next_token = get_upload_sequence_token()
    client.put_log_events(
        logGroupName=LOG_GROUP_NAME,
        logStreamName=LOG_STREAM_NAME,
        logEvents=events,
        sequenceToken=next_token,
    )
