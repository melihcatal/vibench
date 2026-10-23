import os
import boto3

USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

cognito_client = boto3.client("cognito-idp", region_name=REGION)
