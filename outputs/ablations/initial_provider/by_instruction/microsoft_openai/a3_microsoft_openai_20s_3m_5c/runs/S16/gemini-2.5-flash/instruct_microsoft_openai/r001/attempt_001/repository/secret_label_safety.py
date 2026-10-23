import os
from typing import List, Dict, Any
from security_client import SecurityClient

def check_secret_label_safety(secret_name: str, unsafe_keywords: List[str]) -> Dict[str, Any]:
    """Checks secret labels (tags) and potentially notes for unsafe text.

    Args:
        secret_name: The name of the secret in Azure Key Vault.
        unsafe_keywords: A list of keywords considered unsafe.

    Returns:
        A dictionary indicating if unsafe text was found and where.
    """
    client = SecurityClient()
    secret = client.get_secret(secret_name)

    unsafe_findings = {
        "secret_name": secret_name,
        "unsafe_tags_found": False,
        "found_keywords_in_tags": []
    }

    if secret.tags:
        for key, value in secret.tags.items():
            for keyword in unsafe_keywords:
                if keyword.lower() in key.lower() or keyword.lower() in value.lower():
                    unsafe_findings["unsafe_tags_found"] = True
                    unsafe_findings["found_keywords_in_tags"].append(f"{key}:{value} (keyword: {keyword})")

    # The 'value' of a secret could be considered its 'notes' if it's not a direct key.
    # However, for direct secret values, checking for unsafe keywords might be inappropriate.
    # If 'notes' were a separate field in Azure Key Vault secret properties, we would check that.
    # For this exercise, we will only check tags as explicit 'labels' and not the secret value itself.

    return unsafe_findings

if __name__ == "__main__":
    # Example usage: Ensure AZURE_KEYVAULT_URI is set in your environment.
    # And a secret named 'my-sensitive-secret' with tags like {"purpose": "test-credentials"}.
    test_secret_name = os.environ.get("SENSITIVE_SECRET_NAME", "my-sensitive-secret")
    potential_unsafe_keywords = ["password", "credential", "admin", "root", "prod"]

    try:
        safety_report = check_secret_label_safety(test_secret_name, potential_unsafe_keywords)
        print(f"Safety Report for Secret '{safety_report['secret_name']}':")
        if safety_report["unsafe_tags_found"]:
            print(f"  UNSAFE TAGS DETECTED! Found keywords: {safety_report['found_keywords_in_tags']}")
        else:
            print("  No unsafe keywords found in tags.")
    except Exception as e:
        print(f"Error checking secret label safety: {e}")
