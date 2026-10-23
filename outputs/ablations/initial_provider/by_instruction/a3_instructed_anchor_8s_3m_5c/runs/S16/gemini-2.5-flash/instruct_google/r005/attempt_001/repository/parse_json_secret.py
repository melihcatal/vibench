from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os
import json

def parse_json_secret(key_vault_name: str, secret_name: str) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Azure Key Vault.
    """
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    
    retrieved_secret = client.get_secret(secret_name)
    return json.loads(retrieved_secret.value)

if __name__ == "__main__":
    # Example usage:
    # key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
    # secret_name = "myJsonSecret"
    # json_secret = parse_json_secret(key_vault_name, secret_name)
    # print(f"Parsed JSON Secret: {json_secret}")
    pass
