import os
import boto3

COGNITO_USER_POOL_ID = os.environ["COGNITO_USER_POOL_ID"]
COGNITO_CLIENT_ID = os.environ["COGNITO_CLIENT_ID"]
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def get_cognito_client():
    return boto3.client("cognito-idp", region_name=AWS_REGION)
