from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json

def fetch_db_secret(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret_value = client.get_secret(payload['secret_name']).value
            db_credentials = json.loads(secret_value)
    return {
        'username': db_credentials.get('username'),
        'password': db_credentials.get('password'),
        'host': db_credentials.get('host'),
        'port': db_credentials.get('port'),
        'database': db_credentials.get('database')
    }
