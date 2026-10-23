from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


# Rotate Secret Version
def rotate_secret_version(secret_name, version):
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url=os.getenv("AZURE_KEY_VAULT_URL"), credential=credential
    )
    secret = client.get_secret(secret_name, version=version)
    return secret.value
