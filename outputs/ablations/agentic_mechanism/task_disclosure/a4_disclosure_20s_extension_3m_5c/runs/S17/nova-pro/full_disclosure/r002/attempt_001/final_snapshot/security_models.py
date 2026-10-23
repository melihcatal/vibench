from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

class KeyManagementRequest:
    def __init__(self, key_name, key_type):
        self.key_name = key_name
        self.key_type = key_type

    def create_key(self):
        credential = DefaultAzureCredential()
        client = KeyClient(vault_url="https://<your-key-vault-name>.vault.azure.net", credential=credential)
        return client.create_key(name=self.key_name, key_type=self.key_type)

class KeyManagementResponse:
    def __init__(self, key):
        self.key = key

    def get_key_details(self):
        return {
            'key_name': self.key.name,
            'key_type': self.key.key_type,
            'created': self.key.created_on
        }

class NormalizationHelper:
    @staticmethod
    def normalize_key_name(key_name):
        return key_name.lower().replace(' ', '-')
