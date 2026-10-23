from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def rotate_secret_version(vault_url, secret_name, version):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(secret_name, version=version)
    return secret.value