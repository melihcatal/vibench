import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def fetch_db_secret(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            value = client.get_secret(payload['secret_id']).value
    if payload.get('key_field'):
        value = json.loads(value)[payload['key_field']]
    return {'db_secret': value}
