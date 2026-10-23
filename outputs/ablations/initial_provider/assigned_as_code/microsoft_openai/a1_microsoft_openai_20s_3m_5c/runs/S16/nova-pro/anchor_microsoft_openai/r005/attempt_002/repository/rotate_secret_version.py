from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def rotate_secret_version(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            value = client.get_secret(payload['secret_id'], version=payload.get('version')).value
    return {'rotated_secret': value}