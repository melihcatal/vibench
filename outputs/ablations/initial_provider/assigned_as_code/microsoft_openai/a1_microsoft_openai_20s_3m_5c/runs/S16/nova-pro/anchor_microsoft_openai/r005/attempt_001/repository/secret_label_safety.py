import re
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from security_client import get_security_client


def check_secret_labels(vault_url, secret_id):
    client = get_security_client(vault_url)
    secret = client.get_secret(secret_id)
    labels = secret.properties.tags
    unsafe_labels = [label for label in labels if re.search(r'[a-zA-Z0-9]', label)]
    return unsafe_labels
