from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def get_secret_client():
    credential = DefaultAzureCredential()
    return SecretClient(
        vault_url=os.environ["AZURE_KEY_VAULT_URL"], credential=credential
    )
