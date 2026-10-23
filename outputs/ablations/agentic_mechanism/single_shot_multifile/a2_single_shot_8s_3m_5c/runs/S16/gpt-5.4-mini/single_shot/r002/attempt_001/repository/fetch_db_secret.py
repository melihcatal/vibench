from security_client import get_secret_manager_client
from security_models import SecretFetchRequest, SecretValue


def fetch_db_secret(secret_name: str, version: str = "latest") -> SecretValue:
    client = get_secret_manager_client()
    request = SecretFetchRequest(secret_name=secret_name, version=version)
    return client.fetch_secret(request)
