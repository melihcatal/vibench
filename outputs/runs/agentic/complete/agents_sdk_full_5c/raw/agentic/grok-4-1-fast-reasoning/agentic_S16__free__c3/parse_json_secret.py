import json
import os
from security_client import get_secrets_client
from typing import Dict, Any

def parse_json_secret(secret_name: str = None) -&gt; Dict[str, Any]:
    if secret_name is None:
        secret_name = os.getenv('JSON_SECRET_NAME')
    if not secret_name:
        raise ValueError('JSON_SECRET_NAME must be set')
    client = get_secrets_client()
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])