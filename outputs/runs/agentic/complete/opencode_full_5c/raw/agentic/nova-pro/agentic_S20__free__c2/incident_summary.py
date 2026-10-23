import boto3
import os
from observability_client import get_cw_logs_client
from observability_models import LogEvent

cw_logs = get_cw_logs_client()

log_group_name = os.getenv("LOG_GROUP_NAME", "MyLogGroup")

response = cw_logs.filter_log_events(
    logGroupName=log_group_name,
    startTime=int(time.time() * 1000) - 3600000,  # 1 hour ago
    endTime=int(time.time() * 1000),
    filterPattern="ERROR",
)

log_events = [LogEvent.from_dict(event) for event in response["events"]]

summary = {
    "total_errors": len(log_events),
    "error_messages": [event.message for event in log_events],
}

print(summary)
