from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def get_secret_client():
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url="https://<your-key-vault-name>.vault.azure.net/",
        credential=credential,
    )
    return client
