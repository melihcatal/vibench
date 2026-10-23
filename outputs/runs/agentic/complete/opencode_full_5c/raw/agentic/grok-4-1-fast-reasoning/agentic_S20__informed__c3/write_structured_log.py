import time
from typing import Optional, Dict, Any
from observability_models import StructuredLog, log_to_aws_event
from observability_client import put_log_events


def write_structured_log(
    message: str,
    level: str = "INFO",
    service: str = "app",
    correlation_id: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
):
    timestamp = int(time.time() * 1000)
    log = StructuredLog(
        timestamp=timestamp,
        level=level,
        message=message,
        service=service,
        correlation_id=correlation_id,
        data=data,
    )
    event = log_to_aws_event(log)
    put_log_events([event])
