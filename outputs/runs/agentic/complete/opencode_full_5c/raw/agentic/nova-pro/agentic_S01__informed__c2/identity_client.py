import os
import boto3


def get_cognito_client():
    return boto3.client("cognito-idp", region_name="us-west-2")


def get_aws_client_id():
    return os.getenv("AWS_CLIENT_ID")
