import boto3

cw_logs = boto3.client("logs", region_name="us-west-2")

log_group_name = "MyLogGroup"


def get_client():
    return cw_logs


def get_log_group_name():
    return log_group_name
