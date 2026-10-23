from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def rotation_summary(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret = client.get_secret(payload['secret_id'])
    return {'summary': {'name': secret.name, 'version': secret.properties.version, 'enabled': secret.properties.enabled}}
