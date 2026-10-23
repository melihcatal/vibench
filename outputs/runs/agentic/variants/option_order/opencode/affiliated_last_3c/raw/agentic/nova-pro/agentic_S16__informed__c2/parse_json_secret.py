import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import json


# Retrieves and parses a JSON-formatted secret from Azure Key Vault Secrets
def parse_json_secret(secret_name):
    key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    secret = client.get_secret(secret_name)
    return json.loads(secret.value)
