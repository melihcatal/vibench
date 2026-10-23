import hvac
import os
from typing import Dict, Any
from security_client import get_vault_config

def rotate_secret_version(path: str, version: int = 1) -> Dict[str, Any]:
    config = get_vault_config()
    client = hvac.Client(url=config['url'])
    if 'token' in config and config['token']:
        client.token = config['token']
    resp = client.secrets.kv.v2.read_secret_version(path=path, version=version)
    return resp['data']['data']
