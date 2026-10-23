from security_client import get_secret_manager_client
from security_models import SecretFetchRequest, SecretVersionRequest


def rotate_secret_version(secret_name: str, version: str = "latest", stage: str = "CURRENT"):
    client = get_secret_manager_client()
    request = SecretVersionRequest(secret_name=secret_name, version=version, stage=stage)
    return client.fetch_secret_version(request)
