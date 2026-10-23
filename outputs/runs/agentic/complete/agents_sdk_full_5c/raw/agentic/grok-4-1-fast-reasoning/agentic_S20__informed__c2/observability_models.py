from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import time

class StructuredLog(TypedDict):
    level: str
    message: str
    correlation_id: Optional[str]
    service: Optional[str]

class LogEvent(TypedDict):
    timestamp: int
    message: str

class QueryParams(TypedDict):
    start_time: int
    end_time: int
    log_group: str

def get_time_range(hours_back: int = 1) -> tuple[int, int]:
    now = datetime.utcnow()
    end_time = int(now.timestamp() * 1000)
    start_time = int((now - timedelta(hours=hours_back)).timestamp() * 1000)
    return start_time, end_time

def parse_log_event(event: Dict[str, Any]) -> StructuredLog:
    try:
        parsed = json.loads(event['message'])
        return parsed  # type: ignore
    except (json.JSONDecodeError, KeyError):
        return {'level': 'UNKNOWN', 'message': event.get('message', ''), 'correlation_id': None, 'service': None}

def prepare_log_events(structured_logs: List[StructuredLog], base_timestamp: Optional[int] = None) -> List[LogEvent]:
    if base_timestamp is None:
        base_timestamp = int(time.time() * 1000)
    events = []
    for idx, log_data in enumerate(structured_logs):
        timestamp = base_timestamp + idx
        message = json.dumps(log_data)
        events.append(LogEvent(timestamp=timestamp, message=message))
    return events
