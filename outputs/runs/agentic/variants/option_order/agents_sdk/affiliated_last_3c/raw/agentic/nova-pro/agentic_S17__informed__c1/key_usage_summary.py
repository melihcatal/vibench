import azure.identity
from azure.keyvault.administration import KeyVaultAccessControlClient

def get_key_usage_summary(vault_url):
    credential = azure.identity.DefaultAzureCredential()
    client = KeyVaultAccessControlClient(vault_url, credential)
    return client.get_key_usage_summary()