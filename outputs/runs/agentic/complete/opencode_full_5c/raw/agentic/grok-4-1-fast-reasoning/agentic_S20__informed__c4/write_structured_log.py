from datetime import datetime
from typing import Dict, Any
from .observability_client import put_log_events, get_upload_sequence_token
from .observability_models import log_event_to_cloudwatch


def write_structured_log(
    level: str = "INFO",
    service: str = "app",
    event_type: str = "generic",
    **kwargs: Any,
) -> None:
    structured_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "service": service,
        "event_type": event_type,
        **kwargs,
    }
    cw_event = log_event_to_cloudwatch(structured_log)
    seq_token = get_upload_sequence_token()
    new_token = put_log_events([cw_event], seq_token)
    print(f"Structured log written. Next sequence token: {new_token}")
