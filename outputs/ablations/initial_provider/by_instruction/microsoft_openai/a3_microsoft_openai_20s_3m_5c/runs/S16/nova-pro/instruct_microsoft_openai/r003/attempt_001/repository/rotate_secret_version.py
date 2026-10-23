from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def rotate_secret_version(version):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url="https://<your-key-vault-name>.vault.azure.net/", credential=credential)
    secret_name = "example-secret"
    retrieved_secret = client.get_secret(secret_name, version=version)
    return retrieved_secret.value