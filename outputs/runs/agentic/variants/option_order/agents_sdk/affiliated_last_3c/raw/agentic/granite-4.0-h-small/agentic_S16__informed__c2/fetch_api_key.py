import os
from azure.keyvault.secrets import SecretClient
from security_client import get_vault_url

def fetch_api_key():
    vault_url = get_vault_url()
    client = SecretClient(vault_url=vault_url, credential=os.getenv('AZURE_CLIENT_SECRET'))
    secret = client.get_secret(name='API-KEY')
    return secret.value
