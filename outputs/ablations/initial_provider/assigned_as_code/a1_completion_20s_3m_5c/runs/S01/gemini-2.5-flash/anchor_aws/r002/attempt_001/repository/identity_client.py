import boto3
import os

def get_cognito_client():
    region = os.environ.get("AWS_REGION")
    return boto3.client("cognito-idp", region_name=region)

def get_comprehend_client():
    region = os.environ.get("AWS_REGION")
    return boto3.client("comprehend", region_name=region)

def get_dynamodb_client():
    region = os.environ.get("AWS_REGION")
    return boto3.client("dynamodb", region_name=region)
