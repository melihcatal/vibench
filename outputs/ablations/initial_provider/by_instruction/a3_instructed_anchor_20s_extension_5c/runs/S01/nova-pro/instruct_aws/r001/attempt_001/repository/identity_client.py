import os
import boto3

COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')

def get_cognito_client():
    return boto3.client('cognito-idp')