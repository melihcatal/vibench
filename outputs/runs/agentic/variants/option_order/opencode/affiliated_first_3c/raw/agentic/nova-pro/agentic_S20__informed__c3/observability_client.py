import boto3
import os

client = boto3.client(
    "logs",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def write_log(log_group, log_stream, message):
    client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[{"timestamp": int(round(time.time() * 1000)), "message": message}],
    )
