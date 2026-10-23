import boto3

cw_logs = boto3.client("logs", region_name="us-west-2")

log_group_name = "MyLogGroup"


def write_log_event(log_stream_name, log_event):
    response = cw_logs.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[log_event],
    )
    return response


if __name__ == "__main__":
    log_stream_name = "MyLogStream"
    log_event = {
        "timestamp": int(time.time() * 1000),
        "message": json.dumps({"event": "example", "severity": "INFO"}),
    }
    response = write_log_event(log_stream_name, log_event)
    print(response)
