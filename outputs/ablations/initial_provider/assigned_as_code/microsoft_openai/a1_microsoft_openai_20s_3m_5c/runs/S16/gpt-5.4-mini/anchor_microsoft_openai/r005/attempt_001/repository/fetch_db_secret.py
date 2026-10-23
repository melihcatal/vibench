from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_client import load_config, secret_name


def fetch_db_secret(payload, config=None):
    config = load_config(config)
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            value = client.get_secret(secret_name(payload)).value
    return {'db_secret': value}
