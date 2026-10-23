from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class SecurityClient:
    def __init__(self, vault_url):
        self.vault_url = vault_url
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)


def get_security_client(vault_url):
    return SecurityClient(vault_url)
