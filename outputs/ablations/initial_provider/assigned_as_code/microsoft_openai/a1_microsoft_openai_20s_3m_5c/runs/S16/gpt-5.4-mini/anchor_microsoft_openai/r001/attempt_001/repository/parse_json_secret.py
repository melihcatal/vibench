import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_client import load_config, get_secret_name


def parse_json_secret(payload, config=None):
    config = load_config(config)
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            value = client.get_secret(get_secret_name(payload, 'secret_id')).value
    return {'secret_json': json.loads(value)}
