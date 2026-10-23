from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def fetch_db_secret():
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url=os.environ["AZURE_KEY_VAULT_URL"], credential=credential
    )
    secret = client.get_secret("db-secret")
    return secret.value
