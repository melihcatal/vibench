import boto3
import time
import json

cw_logs = boto3.client("logs", region_name="us-west-2")

log_group_name = "MyLogGroup"
log_stream_name = "MyLogStream"

correlation_id = "abc123"

log_events = [
    {
        "timestamp": int(time.time() * 1000),
        "message": json.dumps(
            {"event": "request_start", "correlation_id": correlation_id}
        ),
    },
    {
        "timestamp": int(time.time() * 1000),
        "message": json.dumps(
            {"event": "request_end", "correlation_id": correlation_id}
        ),
    },
]

response = cw_logs.put_log_events(
    logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=log_events
)

print(response)
