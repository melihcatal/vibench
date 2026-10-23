import os
import boto3

def get_config():
    return {
        'region': os.getenv('AWS_REGION'),
        'domain_prefix': os.getenv('AWS_COGNITO_DOMAIN_PREFIX'),
        'client_id': os.getenv('AWS_COGNITO_CLIENT_ID')
    }

def create_client():
    return boto3.client('cognito-idp')