from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_client import load_config, secret_name, version_name, staged_name


def rotate_secret_version(payload, config=None):
    config = load_config(config)
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            if version_name(payload):
                value = client.get_secret(secret_name(payload), version=version_name(payload)).value
            elif staged_name(payload):
                value = client.get_secret(secret_name(payload), version=staged_name(payload)).value
            else:
                value = client.get_secret(secret_name(payload)).value
    return {'secret_version': value}
