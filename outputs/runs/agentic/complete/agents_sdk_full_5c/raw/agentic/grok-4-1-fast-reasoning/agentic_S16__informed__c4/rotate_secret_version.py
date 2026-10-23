import requests
import os
from security_client import get_doppler_token, get_doppler_config
from typing import Dict, Any

def read_secret_version(config_name: str, secret_name: str, version: str = 'current') -> Dict[str, Any]:
    token = get_doppler_token()
    headers = {'Authorization': f'token {token}'}
    base_url = f"https://api.doppler.com/v3/configs/{config_name}/secrets/{secret_name}"
    url = f"{base_url}?version={version}" if version != 'current' else base_url
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
