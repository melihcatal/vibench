import boto3


def create_observability_client():
    return boto3.client("cloudwatch")
