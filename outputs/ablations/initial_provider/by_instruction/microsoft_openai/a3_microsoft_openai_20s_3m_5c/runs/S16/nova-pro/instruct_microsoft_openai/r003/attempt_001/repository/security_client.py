from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class SecurityClient:
    def __init__(self, vault_url):
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=vault_url, credential=self.credential)

    def get_secret(self, secret_name):
        return self.client.get_secret(secret_name).value