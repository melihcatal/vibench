import boto3
import time

cw_logs = boto3.client("logs", region_name="us-west-2")

log_group_name = "MyLogGroup"
log_stream_name = "MyLogStream"

correlation_id = "abc123"

log_events = [
    {
        "timestamp": int(time.time() * 1000),
        "message": f"User login attempt with correlation ID: {correlation_id}",
    },
    {
        "timestamp": int(time.time() * 1000),
        "message": f"User login success with correlation ID: {correlation_id}",
    },
]

response = cw_logs.put_log_events(
    logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=log_events
)

print(response)
