import boto3

cw_logs = boto3.client("logs", region_name="us-west-2")

log_group_name = "MyLogGroup"


def get_cw_logs_client():
    return cw_logs


def create_log_group(log_group_name):
    response = cw_logs.create_log_group(logGroupName=log_group_name)
    return response


def create_log_stream(log_stream_name):
    response = cw_logs.create_log_stream(
        logGroupName=log_group_name, logStreamName=log_stream_name
    )
    return response
