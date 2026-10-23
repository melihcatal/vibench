import os
from azure.identity import DefaultAzureCredential


# Security Client Helper
def get_security_client(vault_url):
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)
