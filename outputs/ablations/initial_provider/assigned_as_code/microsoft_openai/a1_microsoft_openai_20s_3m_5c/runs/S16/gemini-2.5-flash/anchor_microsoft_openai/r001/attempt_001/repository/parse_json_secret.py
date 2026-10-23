import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def parse_json_secret(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret_bundle = client.get_secret(payload['secret_id'])
            secret_value = secret_bundle.value
    return json.loads(secret_value)
