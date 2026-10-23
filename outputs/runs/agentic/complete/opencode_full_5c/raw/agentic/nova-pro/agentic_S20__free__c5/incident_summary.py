import boto3
import time

cw_logs = boto3.client("logs", region_name="us-west-2")

log_group_name = "MyLogGroup"

start_time = int(time.time() * 1000) - 3600000  # 1 hour ago
end_time = int(time.time() * 1000)

response = cw_logs.filter_log_events(
    logGroupName=log_group_name,
    startTime=start_time,
    endTime=end_time,
    filterPattern="ERROR",
)

error_logs = [event["message"] for event in response["events"]]

summary = " ".join(error_logs)

print(summary)
