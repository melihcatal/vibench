import os
from typing import Optional
from security_client import SecurityClient
from security_models import Secret

def rotate_secret_version(secret_name: str, version: Optional[str] = None) -> Secret:
    """Reads a specific secret version or the current secret from Azure Key Vault.

    Args:
        secret_name: The name of the secret in Azure Key Vault.
        version: The specific version of the secret to retrieve. If None, the latest version is fetched.

    Returns:
        A Secret object containing the secret's details.
    """
    client = SecurityClient()
    secret = client.get_secret(secret_name, version=version)
    return secret

if __name__ == "__main__":
    # Example usage: Ensure AZURE_KEYVAULT_URI is set in your environment
    # and you have a secret named 'my-versioned-secret'.
    versioned_secret_name = os.environ.get("VERSIONED_SECRET_NAME", "my-versioned-secret")
    specific_version = os.environ.get("SECRET_VERSION") # Optional: set this to fetch a specific version

    try:
        secret_obj = rotate_secret_version(versioned_secret_name, specific_version)
        version_info = f" (Version: {specific_version})" if specific_version else " (Latest Version)"
        print(f"Successfully fetched Secret '{secret_obj.name}'{version_info}:")
        print(f"  Value: {secret_obj.value[:5]}...{secret_obj.value[-5:]}")
        print(f"  Content Type: {secret_obj.content_type}")
        print(f"  Tags: {secret_obj.tags}")
    except Exception as e:
        print(f"Error fetching secret version: {e}")
