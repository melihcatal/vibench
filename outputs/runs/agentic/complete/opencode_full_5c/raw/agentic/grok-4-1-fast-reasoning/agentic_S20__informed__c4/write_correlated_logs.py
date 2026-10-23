from datetime import datetime
from typing import Dict, Any, List
from .observability_client import put_log_events, get_upload_sequence_token
from .observability_models import log_event_to_cloudwatch


def write_correlated_logs(
    correlation_id: str, log_events: List[Dict[str, Any]]
) -> None:
    for event in log_events:
        event["correlation_id"] = correlation_id
        event["timestamp"] = datetime.utcnow().isoformat()
    cw_events = [log_event_to_cloudwatch(e) for e in log_events]
    seq_token = get_upload_sequence_token()
    new_token = put_log_events(cw_events, seq_token)
    print(
        f"Correlated logs written with ID {correlation_id}. Next sequence token: {new_token}"
    )
