import os
import re
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url=os.getenv('AZURE_KEYVAULT_URL'), credential=credential)

def secret_label_safety(secret_name):
    properties = client.get_secret_properties(secret_name)
    labels = properties.tags.get('labels', '')
    unsafe_pattern = re.compile(r'(password|secret|key)')
    return not bool(unsafe_pattern.search(labels))