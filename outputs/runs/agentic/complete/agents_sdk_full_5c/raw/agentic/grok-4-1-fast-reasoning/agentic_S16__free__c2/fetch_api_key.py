import boto3
import os

region_name = os.getenv('AWS_REGION', 'us-east-1')
client = boto3.client('secretsmanager', region_name=region_name)

def fetch_api_key(secret_name: str) -> str:
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']