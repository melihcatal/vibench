import os
from ibm_secrets_manager.secrets_manager import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from security_models import SecretConfig
from security_client import load_provider_env
from typing import Optional

def read_secret_version(secret_name: str, version: str) -> str:
    provider = 'ibm'
    env_config = load_provider_env(provider)
    apikey = env_config.get('IBM_SECRETS_MANAGER_APIKEY')
    url = env_config.get('IBM_SECRETS_MANAGER_URL')
    config = SecretConfig(name=secret_name, version=version)
    authenticator = IAMAuthenticator(apikey)
    client = SecretsManagerV1(authenticator=authenticator, url=url)
    get_secret_response = client.get_secret(secret_id=config.name, version=config.version).get_result()
    return get_secret_response['secret']['payload']