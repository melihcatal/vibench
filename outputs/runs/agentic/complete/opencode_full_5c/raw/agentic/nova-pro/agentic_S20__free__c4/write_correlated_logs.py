import boto3
import time
import json

cw_logs = boto3.client("logs", region_name="us-west-2")

log_group_name = "my-log-group"
log_stream_name = "my-log-stream"

correlation_id = "1234567890"

log_event1 = {
    "timestamp": int(time.time() * 1000),
    "message": json.dumps(
        {
            "event": "correlated_log",
            "correlation_id": correlation_id,
            "data": {"key": "value1"},
        }
    ),
}
log_event2 = {
    "timestamp": int(time.time() * 1000),
    "message": json.dumps(
        {
            "event": "correlated_log",
            "correlation_id": correlation_id,
            "data": {"key": "value2"},
        }
    ),
}

cw_logs.put_log_events(
    logGroupName=log_group_name,
    logStreamName=log_stream_name,
    logEvents=[log_event1, log_event2],
)
