from security_client import AzureKeyVaultSecurityClient
import os
from typing import List

def check_secret_label_safety(secret_name: str, unsafe_keywords: List[str] = None, vault_url: str = None) -> dict:
    client = AzureKeyVaultSecurityClient(vault_url)
    secret_properties = client.client.get_secret_properties(secret_name)

    if unsafe_keywords is None:
        unsafe_keywords = ["password", "credential", "token", "key", "secret_value"]

    unsafe_labels = []
    if secret_properties.tags:
        for key, value in secret_properties.tags.items():
            for keyword in unsafe_keywords:
                if keyword in key.lower() or keyword in value.lower():
                    unsafe_labels.append(f"Tag '{key}': '{value}' contains unsafe keyword '{keyword}'")

    # Azure Key Vault secret properties don't have a direct 'notes' field.
    # We'll simulate checking a 'description' tag or similar if it were present.
    # For this example, we focus on tags.
    
    return {
        "secret_id": secret_name,
        "has_unsafe_labels": len(unsafe_labels) > 0,
        "unsafe_findings": unsafe_labels
    }
