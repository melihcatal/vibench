import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

load_dotenv()

AZURE_KEY_VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL")

credential = DefaultAzureCredential()
client = SecretClient(vault_url=AZURE_KEY_VAULT_URL, credential=credential)


def fetch_api_key(secret_name: str) -> str:
    """Fetch an API key from Azure Key Vault Secrets.

    Returns the secret value as a string.
    """
    received = client.get_secret(secret_name)
    return received.value
