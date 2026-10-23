
import os
import hvac

def get_vault_client() -> hvac.Client | None:
    """
    Initializes and returns an authenticated HashiCorp Vault client.

    Reads configuration from environment variables:
    - VAULT_ADDR: The URL of the Vault server.
    - VAULT_TOKEN: The token to authenticate with.

    Returns:
        An authenticated hvac.Client instance, or None if configuration is missing.
    """
    vault_addr = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")

    if not vault_addr or not vault_token:
        print("VAULT_ADDR and VAULT_TOKEN environment variables must be set.")
        return None
    
    try:
        client = hvac.Client(url=vault_addr, token=vault_token)
        if client.is_authenticated():
            return client
        else:
            print("Vault authentication failed. Check your VAULT_TOKEN.")
            return None
    except Exception as e:
        print(f"Error initializing Vault client: {e}")
        return None
