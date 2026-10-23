import boto3
import time

cw_logs = boto3.client("logs", region_name="us-west-2")

log_group_name = "my-log-group"
log_stream_name = "my-log-stream"

start_time = int(time.time() * 1000) - 3600000  # 1 hour ago
end_time = int(time.time() * 1000)

response = cw_logs.filter_log_events(
    logGroupName=log_group_name,
    logStreamNames=[log_stream_name],
    startTime=start_time,
    endTime=end_time,
    filterPattern="ERROR",
)

for event in response["events"]:
    print(event["message"])
