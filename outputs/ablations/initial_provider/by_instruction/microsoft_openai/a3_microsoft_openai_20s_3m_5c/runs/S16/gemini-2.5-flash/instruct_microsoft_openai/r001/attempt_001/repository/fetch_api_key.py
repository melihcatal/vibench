import os
from security_client import SecurityClient

def fetch_api_key(secret_name: str) -> str:
    """Fetches an API key from Azure Key Vault.

    Args:
        secret_name: The name of the secret in Azure Key Vault.

    Returns:
        The API key as a string.
    """
    client = SecurityClient()
    secret = client.get_secret(secret_name)
    return secret.value

if __name__ == "__main__":
    # Example usage: Ensure AZURE_KEYVAULT_URI is set in your environment
    # and you have access to the specified secret.
    api_key_name = os.environ.get("API_KEY_NAME", "my-api-key")
    try:
        api_key = fetch_api_key(api_key_name)
        print(f"Successfully fetched API Key: {api_key[:5]}...{api_key[-5:]}")
    except Exception as e:
        print(f"Error fetching API key: {e}")
