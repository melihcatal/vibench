import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from observability_client import get_aws_cloudwatch_client
from observability_models import FilteredLogEvent


def fetch_recent_logs(
    log_group_name: str,
    filter_pattern: Optional[str] = None,
    duration_minutes: int = 60,
    limit: int = 100,
    region_name: Optional[str] = None,
) -> List[FilteredLogEvent]:
    client = get_aws_cloudwatch_client(region_name or os.environ.get("AWS_REGION", "us-east-1"))

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)

    params = {
        "logGroupName": log_group_name,
        "startTime": int(start_time.timestamp() * 1000),
        "endTime": int(end_time.timestamp() * 1000),
        "limit": limit,
    }
    if filter_pattern:
        params["filterPattern"] = filter_pattern

    response = client.filter_log_events(**params)

    fetched_events: List[FilteredLogEvent] = []
    for event in response.get("events", []):
        # Assuming message is a JSON string that might contain structured data
        # For simplicity, we're just parsing the message string here.
        fetched_events.append(
            FilteredLogEvent(
                message=event["message"],
                timestamp=datetime.fromtimestamp(event["timestamp"] / 1000),
                log_stream_name=event["logStreamName"],
                ingestion_time=datetime.fromtimestamp(event["ingestionTime"] / 1000),
                event_id=event["eventId"],
                log_group_name=log_group_name
            )
        )

    return fetched_events
