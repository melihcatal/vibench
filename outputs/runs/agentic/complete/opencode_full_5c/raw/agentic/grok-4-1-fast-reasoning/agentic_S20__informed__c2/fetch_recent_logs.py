import time
from typing import List, Dict, Any

from observability_client import get_client, LOG_GROUP_NAME, LOG_STREAM_NAME
from observability_models import parse_log_message


def fetch_recent_logs(
    filter_condition: str, hours_ago: int = 24
) -> List[Dict[str, Any]]:
    client = get_client()
    end_time_ms = int(time.time() * 1000)
    start_time_ms = end_time_ms - (hours_ago * 3600 * 1000)
    filter_pattern = f"[{filter_condition}]"
    response = client.filter_log_events(
        logGroupName=LOG_GROUP_NAME,
        logStreamNames=[LOG_STREAM_NAME],
        filterPattern=filter_pattern,
        startTime=start_time_ms,
        endTime=end_time_ms,
        limit=1000,
    )
    events = response.get("events", [])
    parsed = []
    for ev in events:
        parsed_log = parse_log_message(ev["message"])
        parsed_log["ingestionTime"] = ev["ingestionTime"]
        parsed_log["eventId"] = ev["eventId"]
        parsed.append(parsed_log)
    return parsed
