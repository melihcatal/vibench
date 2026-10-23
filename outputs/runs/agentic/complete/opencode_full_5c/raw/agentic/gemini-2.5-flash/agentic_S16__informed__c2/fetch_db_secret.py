from security_client import get_secret_client
from security_models import SecretItem


def fetch_db_secret(secret_name: str) -> SecretItem:
    client = get_secret_client()
    try:
        secret = client.get_secret(secret_name)
        return SecretItem(name=secret.name, value=secret.value)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch database secret '{secret_name}': {e}")
