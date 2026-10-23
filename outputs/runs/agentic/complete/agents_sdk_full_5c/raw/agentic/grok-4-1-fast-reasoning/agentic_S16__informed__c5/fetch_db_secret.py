from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from security_client import parse_db_secret
from security_models import DbSecret

def fetch_db_secret(secret_name: str = None, vault_url: str = None) -> DbSecret:
    if vault_url is None:
        vault_url = os.getenv('AZURE_KEY_VAULT_URL')
    if secret_name is None:
        secret_name = os.getenv('DB_SECRET_NAME', 'db-connection')
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    retrieved_secret = client.get_secret(secret_name)
    return parse_db_secret(retrieved_secret.value)