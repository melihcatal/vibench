import json
from typing import Dict, Any
from observability_client import append_log_event

def write_structured_log(event: Dict[str, Any]):
    """
    Writes a structured JSON log event to Amazon CloudWatch Logs.
    """
    message = json.dumps(event)
    append_log_event(message)
