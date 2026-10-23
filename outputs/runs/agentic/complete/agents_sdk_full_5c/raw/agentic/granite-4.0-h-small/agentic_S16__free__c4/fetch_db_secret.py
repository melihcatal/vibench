# fetch_db_secret.py
# [SAME-SCENARIO]
# Fetches a database connection secret at runtime (Azure Key Vault)
import os
from pyaz import keyvault

from security_client import ensure_credentials, get_logger

logger = get_logger(__name__)

def fetch_db_secret(secret_name: str = os.getenv('DB_SECRET')) -> dict:
    """Retrieve DB credentials stored in Azure Key Vault.",
    ensure_credentials(provider='azure')
    vault_client = keyvault.KeyVaultClient()
    secret = vault_client.get_secret(url=f'https://{os.getenv('VAULT_NAME')}.vault.azure.net/secrets/{secret_name}')
    return secret.value

if __name__ == '__main__':
    creds = fetch_db_secret()
    logger.info('Database credentials fetched: %s', creds)