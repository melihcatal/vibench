from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_models import parse_json_secret_value


def parse_json_secret(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            value = client.get_secret(payload['secret_id']).value
    return {'secret': parse_json_secret_value(value)}
