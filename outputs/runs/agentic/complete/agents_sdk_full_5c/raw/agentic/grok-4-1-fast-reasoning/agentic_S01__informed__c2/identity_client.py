import os
import boto3

COGNITO_REGION = os.getenv('AWS_REGION', 'us-east-1')
USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
if not USER_POOL_ID:
    raise ValueError('COGNITO_USER_POOL_ID environment variable is required')

cognito_client = boto3.client(
    'cognito-idp',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=COGNITO_REGION
)