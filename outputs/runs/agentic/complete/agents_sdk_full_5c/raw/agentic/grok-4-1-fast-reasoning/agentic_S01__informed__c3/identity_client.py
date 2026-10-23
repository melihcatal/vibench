import os
import boto3
from typing import Optional

def create_cognito_client() -&gt; boto3.client:
    return boto3.client(
        'cognito-idp',
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
    )

def get_app_client_id() -&gt; str:
    return os.getenv('COGNITO_APP_CLIENT_ID')