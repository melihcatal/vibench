import boto3
import json

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

translated_logs = {}
for event in response["events"]:
    message = event["message"]
    translated_message = message.replace(
        "error", "erreur"
    )  # Simple translation example
    translated_logs[event["id"]] = translated_message

print(json.dumps(translated_logs, indent=2))
