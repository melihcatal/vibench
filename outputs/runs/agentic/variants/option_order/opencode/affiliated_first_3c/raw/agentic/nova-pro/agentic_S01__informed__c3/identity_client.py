import boto3


def configure_client():
    return boto3.client("cognito-idp", region_name="us-west-2")
