import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from security_client import build_fetched_secret
from security_models import FetchedSecret


def fetch_db_secret(secret_name: str) -> FetchedSecret:
    vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret_bundle = client.get_secret(secret_name)
    value = secret_bundle.value
    metadata = {
        "name": secret_name,
        "version": secret_bundle.version,
        "updated_on": str(secret_bundle.updated_on),
    }
    return build_fetched_secret(value, metadata)
