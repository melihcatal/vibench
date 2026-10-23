from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def rotate_secret_version(version):
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url=os.environ["AZURE_KEY_VAULT_URL"], credential=credential
    )
    secret = client.get_secret("api-key", version=version)
    return secret.value
