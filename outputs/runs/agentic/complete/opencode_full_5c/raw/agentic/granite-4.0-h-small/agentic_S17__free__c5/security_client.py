# [HELPER] security_client.py
import os
from typing import Any

# Azure Key Management Service integration (replace with other providers as needed)


def get_kms_client() -> Any:
    """Creates and returns a client for the chosen KMS provider.

    In this example we use Azure Key Vault. The client is expected to expose
    encrypt, decrypt, sign, verify, generate_data_key, etc. methods.
    """
    from azure.keyvault.secrets import SecretClient
    from azure.identity import DefaultAzureCredential

    # Pull endpoint URL from environment (this makes the integration testable locally)
    vault_url = os.getenv("AZURE_KEYVAULT_URL")
    if not vault_url:
        raise RuntimeError(
            "Set AZURE_KEYVAULT_URL environment variable to your Key Vault URL"
        )
    # DefaultAzureCredential supports Managed Identity, MSI, or local developer credentials
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)
