import json
from typing import List, Dict, Any
from observability_client import append_log_event

def write_correlated_logs(events: List[Dict[str, Any]], correlation_id: str):
    """
    Writes application log events that include a shared request or correlation identifier
    to Amazon CloudWatch Logs.
    """
    for event in events:
        event.setdefault('correlation_id', correlation_id)
        message = json.dumps(event)
        append_log_event(message)
