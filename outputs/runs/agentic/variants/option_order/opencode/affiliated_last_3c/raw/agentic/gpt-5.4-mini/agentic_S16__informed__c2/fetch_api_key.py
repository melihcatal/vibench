from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_client import default_secret_name, secret_vault_url
from security_models import normalize_secret_value


def fetch_api_key(secret_name: str = "api-key"):
    client = SecretClient(
        vault_url=secret_vault_url(), credential=DefaultAzureCredential()
    )
    return normalize_secret_value(
        client.get_secret(default_secret_name(secret_name)).value
    )
