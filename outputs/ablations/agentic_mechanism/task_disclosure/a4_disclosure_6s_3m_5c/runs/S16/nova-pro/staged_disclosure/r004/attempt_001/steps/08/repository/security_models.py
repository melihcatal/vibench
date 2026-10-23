from typing import Dict, Any

import boto3

client = boto3.client('secretsmanager')

def get_secret(secret_name: str) -> Dict[str, Any]:
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

def put_secret(secret_name: str, secret_value: Dict[str, Any]) -> None:
    client.put_secret_value(SecretId=secret_name, SecretString=json.dumps(secret_value))

def normalize_secret(secret: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in secret.items() if k!= 'AWSCURRENT'}