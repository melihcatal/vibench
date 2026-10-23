import json
from typing import Dict, Any

from security_client import get_aws_secretsmanager_client, get_env
from security_models import SecretResponse

def fetch_api_key(secret_id: str = None) -> SecretResponse:
    if secret_id is None:
        secret_id = get_env('API_KEY_SECRET_ID')
        if not secret_id:
            raise ValueError('API_KEY_SECRET_ID environment variable or secret_id argument required')
    client = get_aws_secretsmanager_client()
    resp = client.get_secret_value(SecretId=secret_id)
    return {
        'name': secret_id,
        'value': resp['SecretString'],
        'version_id': resp.get('VersionId')
    }