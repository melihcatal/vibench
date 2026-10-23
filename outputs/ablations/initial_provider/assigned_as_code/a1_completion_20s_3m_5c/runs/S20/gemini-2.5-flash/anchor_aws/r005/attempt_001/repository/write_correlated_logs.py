import json
import time
from typing import Any, Dict, Optional

from observability_client import get_aws_cloudwatch_client
from observability_models import StructuredLogEvent


def write_correlated_logs(
    log_group_name: str,
    log_stream_name: str,
    correlation_id: str,
    events: list[Dict[str, Any]],
    region_name: Optional[str] = None,
):
    client = get_aws_cloudwatch_client(region_name or os.environ.get("AWS_REGION", "us-east-1"))
    log_events = []
    for event_data in events:
        # Add correlation_id to each event
        event_data["correlation_id"] = correlation_id
        log_events.append({
            "timestamp": int(time.time() * 1000),
            "message": json.dumps(event_data),
        })

    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=log_events,
    )

    if response.get("rejectedLogEventsInfo"):
        raise RuntimeError(
            f"CloudWatch rejected log events: {response['rejectedLogEventsInfo']}"
        )
    return {"submitted": True, "correlation_id": correlation_id}
