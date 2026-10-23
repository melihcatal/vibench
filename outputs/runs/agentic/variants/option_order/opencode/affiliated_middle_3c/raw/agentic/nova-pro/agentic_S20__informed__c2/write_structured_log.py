import boto3


def write_log(log_group, log_stream, message):
    client = boto3.client("logs", region_name="us-west-2")
    client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[{"timestamp": int(time.time() * 1000), "message": message}],
    )
