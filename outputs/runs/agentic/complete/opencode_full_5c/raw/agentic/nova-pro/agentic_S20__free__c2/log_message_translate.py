import boto3
import os
from observability_client import get_cw_logs_client

cw_logs = get_cw_logs_client()

log_group_name = os.getenv("LOG_GROUP_NAME", "MyLogGroup")

response = cw_logs.filter_log_events(
    logGroupName=log_group_name,
    startTime=int(time.time() * 1000) - 3600000,  # 1 hour ago
    endTime=int(time.time() * 1000),
    filterPattern="ERROR",
)

log_events = response["events"]

for event in log_events:
    message = event["message"]
    # Translate message to another locale
    translated_message = f"Translated: {message}"
    print(translated_message)
