import os
from dotenv import load_dotenv

# Azure Key Vault example (managed secret store)
load_dotenv()  # loads .env if present
KEY_VAULT_URL = os.getenv('AZURE_KEY_VAULT_URL')

# Using Azure SDK for Key Vault Secrets
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

def fetch_api_key():
    # Retrieve the API key stored under the secret name 'api-key'
    retrieved = client.get_secret('api-key')
    return retrieved.value
