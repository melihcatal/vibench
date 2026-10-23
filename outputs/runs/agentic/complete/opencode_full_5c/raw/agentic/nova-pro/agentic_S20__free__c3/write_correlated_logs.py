import boto3
import time
import json

cw_logs = boto3.client("logs", region_name="us-west-2")

log_group_name = "MyLogGroup"


def write_correlated_logs(log_stream_name, correlation_id):
    log_event1 = {
        "timestamp": int(time.time() * 1000),
        "message": json.dumps(
            {"event": "start", "severity": "INFO", "correlation_id": correlation_id}
        ),
    }
    log_event2 = {
        "timestamp": int(time.time() * 1000),
        "message": json.dumps(
            {"event": "end", "severity": "INFO", "correlation_id": correlation_id}
        ),
    }
    response1 = cw_logs.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[log_event1],
    )
    response2 = cw_logs.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[log_event2],
    )
    return response1, response2


if __name__ == "__main__":
    log_stream_name = "MyLogStream"
    correlation_id = "12345"
    response1, response2 = write_correlated_logs(log_stream_name, correlation_id)
    print(response1, response2)
