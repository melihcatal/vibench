import os
import boto3

def get_cognito_client():
    return boto3.client('cognito-idp', region_name=os.getenv('AWS_REGION'), aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))