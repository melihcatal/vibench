from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def rotate_secret_version(version):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url="https://<your-key-vault-name>.vault.azure.net/", credential=credential)
    secret = client.get_secret("secret-name", version=version).value
    return secret