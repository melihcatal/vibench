import boto3
import os

def get_cognito_client():
    region = os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("cognito-idp", region_name=region)