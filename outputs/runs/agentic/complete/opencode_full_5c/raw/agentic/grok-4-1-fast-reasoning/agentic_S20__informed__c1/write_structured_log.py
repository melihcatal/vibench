from datetime import datetime
from typing import Dict, Any, Optional
from observability_client import put_log_events


def write_structured_log(
    level: str,
    message: str,
    data: Optional[Dict[str, Any]] = None,
    trace_id: Optional[str] = None,
) -> None:
    event = {
        "timestamp": datetime.now().timestamp(),
        "level": level,
        "message": message,
        "data": data or {},
    }
    if trace_id:
        event["trace_id"] = trace_id
    put_log_events([event])
