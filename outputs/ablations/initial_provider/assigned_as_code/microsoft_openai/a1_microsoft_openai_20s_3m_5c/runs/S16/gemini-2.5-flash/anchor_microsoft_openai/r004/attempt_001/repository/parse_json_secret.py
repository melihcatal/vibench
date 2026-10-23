import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def parse_json_secret(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret_value = client.get_secret(payload['secret_name']).value
            parsed_secret = json.loads(secret_value)
    return parsed_secret
