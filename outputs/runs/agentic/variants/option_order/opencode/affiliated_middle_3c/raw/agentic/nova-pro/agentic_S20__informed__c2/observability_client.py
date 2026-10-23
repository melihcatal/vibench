import boto3


def get_client():
    return boto3.client("logs", region_name="us-west-2")
