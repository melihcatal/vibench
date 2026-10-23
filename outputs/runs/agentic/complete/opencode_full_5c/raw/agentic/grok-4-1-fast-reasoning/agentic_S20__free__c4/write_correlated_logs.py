from typing import List, Dict, Any
from observability_client import CloudWatchLogWriter, get_log_group, get_log_stream


def write_correlated_logs(correlation_id: str, log_events: List[Dict[str, Any]]):
    writer = CloudWatchLogWriter(get_log_group(), get_log_stream())
    for event in log_events:
        event_copy = event.copy()
        event_copy["correlation_id"] = correlation_id
        writer.write(event_copy)
