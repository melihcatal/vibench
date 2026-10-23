from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import get_client, LOG_GROUP_NAME, LOG_STREAM_NAME
from observability_models import parse_cloudwatch_event


def query_error_logs(hours_back: int = 1) -> List[Dict[str, Any]]:
    client = get_client()
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours_back)
    start_time_ms = int(start_time.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)

    kwargs = {
        "logGroupName": LOG_GROUP_NAME,
        "logStreamNames": [LOG_STREAM_NAME],
        "filterPattern": '{ $.level = "ERROR" }',
        "startTime": start_time_ms,
        "endTime": end_time_ms,
    }

    events = []
    next_token = None
    while True:
        if next_token:
            kwargs["nextToken"] = next_token
        response = client.filter_log_events(**kwargs)
        for cw_event in response["events"]:
            events.append(parse_cloudwatch_event(cw_event))

        next_token = response.get("nextToken")
        if not next_token:
            break

    return events
