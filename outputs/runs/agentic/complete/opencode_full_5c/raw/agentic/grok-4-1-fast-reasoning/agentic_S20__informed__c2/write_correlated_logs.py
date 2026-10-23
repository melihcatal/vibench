import json
import time
from typing import List, Dict, Any

from observability_client import (
    get_client,
    LOG_GROUP_NAME,
    LOG_STREAM_NAME,
    ensure_resources,
    get_upload_sequence_token,
)
from observability_models import create_structured_log_event


def write_correlated_logs(correlation_id: str, log_entries: List[Dict[str, Any]]):
    ensure_resources()
    client = get_client()
    next_token = get_upload_sequence_token()
    now_ms = int(time.time() * 1000)
    events = []
    for entry in log_entries:
        log_event_dict = create_structured_log_event(
            message=entry["message"],
            level=entry.get("level", "INFO"),
            correlation_id=correlation_id,
            **{k: v for k, v in entry.items() if k not in ("message", "level")},
        )
        log_message = json.dumps(log_event_dict)
        events.append({"timestamp": now_ms, "message": log_message})
    client.put_log_events(
        logGroupName=LOG_GROUP_NAME,
        logStreamName=LOG_STREAM_NAME,
        logEvents=events,
        sequenceToken=next_token,
    )
