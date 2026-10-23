import boto3
import json
import os

def parse_json_secret(secret_name: str) -> dict:
    client = boto3.client(
        service_name='secretsmanager',
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    response = client.get_secret_value(SecretId=secret_name)
    secret_value = response['SecretString']
    return json.loads(secret_value)