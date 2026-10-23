import hvac
import os
import json
from typing import Dict, Any

from security_client import get_secrets_config

def rotate_secret_version(secret_path: str, version: str | None = None) -> str:
    config = get_secrets_config()
    client = hvac.Client(url=config['vault_addr'])
    client.token = os.getenv('VAULT_TOKEN')
    if version is None:
        read_resp = client.secrets.kv.v2.read_secret_version(path=secret_path)
    else:
        read_resp = client.secrets.kv.v2.read_secret_version(path=secret_path, version=version)
    secret_data = read_resp['data']['data']
    if isinstance(secret_data, dict):
        return json.dumps(secret_data)
    return str(secret_data)