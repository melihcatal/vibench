from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


# Fetch Database Secret
def fetch_db_secret(secret_name):
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url=os.getenv("AZURE_KEY_VAULT_URL"), credential=credential
    )
    secret = client.get_secret(secret_name)
    return secret.value
