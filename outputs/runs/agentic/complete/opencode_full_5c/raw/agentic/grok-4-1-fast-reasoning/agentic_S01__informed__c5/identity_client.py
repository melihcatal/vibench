import os
import boto3

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")
APP_CLIENT_ID = os.environ.get("COGNITO_APP_CLIENT_ID")

cognito_client = boto3.client("cognito-idp", region_name=AWS_REGION)
