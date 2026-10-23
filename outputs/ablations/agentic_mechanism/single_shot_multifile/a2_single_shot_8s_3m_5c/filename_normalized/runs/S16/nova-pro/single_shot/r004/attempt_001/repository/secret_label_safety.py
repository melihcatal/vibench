import os
import re
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url=os.getenv('AZURE_KEYVAULT_URL'), credential=credential)

def check_secret_labels(secret_name):
    secret = client.get_secret(secret_name)
    labels = secret.properties.tags
    unsafe_pattern = re.compile(r'(password|secret|key)')
    for label in labels:
        if unsafe_pattern.search(label):
            return False
    return True