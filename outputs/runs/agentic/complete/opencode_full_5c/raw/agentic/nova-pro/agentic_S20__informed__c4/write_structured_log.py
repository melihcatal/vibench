import boto3


def write_log(log_event):
    client = boto3.client("logs", region_name="us-west-2")
    client.put_log_events(
        logGroupName="my-log-group",
        logStreamName="my-log-stream",
        logEvents=[log_event],
    )
