import boto3
import os

from security_models import SecretResponse

def fetch_db_secret(secret_name: str) -> SecretResponse:
    client = boto3.client(
        'secretsmanager',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    
    response = client.get_secret_value(SecretId=secret_name)
    return SecretResponse(
        name=secret_name,
        value=response['SecretString'],
        version=response['VersionId'],
        enabled=response.get('SecretEnabled', True)
    )