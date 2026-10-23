import time
from typing import List, Tuple, Optional, Dict, Any
from observability_models import StructuredLog, log_to_aws_event
from observability_client import put_log_events


def write_correlated_logs(
    log_tuples: List[Tuple[str, str, Optional[Dict[str, Any]]]],
    service: str,
    correlation_id: str,
):
    timestamp = int(time.time() * 1000)
    events = []
    for level, message, data in log_tuples:
        log = StructuredLog(
            timestamp=timestamp,
            level=level,
            message=message,
            service=service,
            correlation_id=correlation_id,
            data=data,
        )
        events.append(log_to_aws_event(log))
    put_log_events(events)
