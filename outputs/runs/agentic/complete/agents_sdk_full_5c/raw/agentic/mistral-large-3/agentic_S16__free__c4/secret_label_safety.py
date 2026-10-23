import os
import re
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def secret_label_safety(vault_url: str = None) -> Dict[str, bool]:
    """
    Checks secret labels and notes in Azure Key Vault for unsafe text patterns.
    
    Args:
        vault_url: Azure Key Vault URL. Defaults to AZURE_KEY_VAULT_URL env var.
    
    Returns:
        A dictionary mapping secret names to safety status (True if safe).
    """
    if vault_url is None:
        vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secrets = client.list_properties_of_secrets()
    
    unsafe_patterns = [
        re.compile(r"password", re.IGNORECASE),
        re.compile(r"secret", re.IGNORECASE),
        re.compile(r"key", re.IGNORECASE)
    ]
    
    results = {}
    for secret in secrets:
        tags = secret.tags or {}
        notes = tags.get("notes", "")
        is_safe = not any(pattern.search(notes) for pattern in unsafe_patterns)
        results[secret.name] = is_safe
    
    return results