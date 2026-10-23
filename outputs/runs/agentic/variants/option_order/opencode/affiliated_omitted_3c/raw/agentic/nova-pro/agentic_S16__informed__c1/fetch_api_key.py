from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def fetch_api_key():
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url=os.environ["AZURE_KEY_VAULT_URL"], credential=credential
    )
    secret = client.get_secret("api-key")
    return secret.value
