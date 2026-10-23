from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_models import extract_field


def fetch_db_secret(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            value = client.get_secret(payload['secret_id']).value
    secret = extract_field(value, payload.get('key_field'))
    return {'db_secret': secret}
