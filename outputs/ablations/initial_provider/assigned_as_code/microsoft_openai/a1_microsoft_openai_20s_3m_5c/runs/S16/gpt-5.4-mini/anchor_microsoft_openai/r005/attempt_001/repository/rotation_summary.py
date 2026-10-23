from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_client import load_config, secret_name


def rotation_summary(payload, config=None):
    config = load_config(config)
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret = client.get_secret(secret_name(payload))
    return {'rotation_summary': {'name': secret.name, 'version': secret.properties.version, 'enabled': secret.properties.enabled}}
