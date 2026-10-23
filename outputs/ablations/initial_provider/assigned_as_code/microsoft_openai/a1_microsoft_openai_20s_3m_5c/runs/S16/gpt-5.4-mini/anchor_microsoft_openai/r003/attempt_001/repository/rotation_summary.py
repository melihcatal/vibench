from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def rotation_summary(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret = client.get_secret(payload['secret_id'])
    return {'secret_id': payload['secret_id'], 'version': secret.properties.version, 'name': secret.name}
