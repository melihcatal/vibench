import requests
import os
from security_client import get_secret_config

def read_staged_secret(config: str = None, secret_name: str = None) -> str:
    if config is None:
        config = get_secret_config('DOPPLER_CONFIG')
    if secret_name is None:
        secret_name = os.getenv('SECRET_NAME', 'mysecret')
    token = os.getenv('DOPPLER_TOKEN')
    url = f"https://api.doppler.com/v3/configs/{config}/secrets"
    params = {'staged': 'true'}
    headers = {
        'Authorization': f'Token {token}',
        'Accept': 'application/json'
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    secrets = data['config']['secrets']
    for secret in secrets:
        if secret['name'] == secret_name:
            return secret['decodedValue']
    raise ValueError(f"Staged secret {secret_name} not found")