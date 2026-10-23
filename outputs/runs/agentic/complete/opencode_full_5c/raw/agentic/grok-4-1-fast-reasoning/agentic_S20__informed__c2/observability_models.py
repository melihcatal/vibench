import json
from datetime import datetime
from typing import Dict, Any, Optional, List


def create_structured_log_event(
    message: str,
    level: str = "INFO",
    correlation_id: Optional[str] = None,
    **extra_fields,
) -> Dict[str, Any]:
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message,
        **extra_fields,
    }
    if correlation_id:
        event["correlation_id"] = correlation_id
    return event


def parse_log_message(message: str) -> Dict[str, Any]:
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        return {"raw_message": message}
