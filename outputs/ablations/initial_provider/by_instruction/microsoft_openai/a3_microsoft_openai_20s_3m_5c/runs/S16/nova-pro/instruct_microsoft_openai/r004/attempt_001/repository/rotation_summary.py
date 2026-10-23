from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def summarize_rotation_status(vault_url, secret_name):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    properties = client.get_secret_properties(secret_name)
    return properties.attributes.enabled