from typing import Any, Dict

import boto3

client = boto3.client('secretsmanager')


def get_secret(secret_id: str) -> Dict[str, Any]:
    response = client.get_secret_value(SecretId=secret_id)
    return json.loads(response['SecretString'])


def put_secret(secret_id: str, secret: Dict[str, Any]) -> Dict[str, Any]:
    response = client.put_secret_value(SecretId=secret_id, SecretString=json.dumps(secret))
    return response


def normalize_secret(secret: Dict[str, Any]) -> Dict[str, Any]:
    normalized_secret = {}
    for key, value in secret.items():
        if isinstance(value, str):
            normalized_secret[key] = value.strip()
        else:
            normalized_secret[key] = value
    return normalized_secret