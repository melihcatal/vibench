import boto3


def summarize_audit_events(log_group_name: str):
    client = boto3.client("logs")
    response = client.describe_log_streams(logGroupName=log_group_name, orderBy="LastEventTime", descending=True)
    return {"provider": "aws-cloudwatch-logs", "streams": response.get("logStreams", [])}
