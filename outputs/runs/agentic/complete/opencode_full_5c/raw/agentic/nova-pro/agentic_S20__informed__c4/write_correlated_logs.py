import boto3


def write_correlated_logs(log_events):
    client = boto3.client("logs", region_name="us-west-2")
    for log_event in log_events:
        client.put_log_events(
            logGroupName="my-log-group",
            logStreamName="my-log-stream",
            logEvents=[log_event],
        )
