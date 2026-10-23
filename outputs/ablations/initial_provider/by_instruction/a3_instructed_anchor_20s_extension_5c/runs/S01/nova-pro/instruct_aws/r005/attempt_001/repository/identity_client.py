import os
import boto3

def get_cognito_client():
    region = os.getenv('AWS_REGION', 'us-west-2')
    client_id = os.getenv('COGNITO_CLIENT_ID')
    client = boto3.client('cognito-idp', region_name=region)
    return client