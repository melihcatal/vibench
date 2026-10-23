from security_client import get_azure_keyvault_client


def fetch_db_secret(secret_name: str) -> str:
    client = get_azure_keyvault_client()
    fetched_secret = client.get_secret(secret_name)
    return fetched_secret.value
