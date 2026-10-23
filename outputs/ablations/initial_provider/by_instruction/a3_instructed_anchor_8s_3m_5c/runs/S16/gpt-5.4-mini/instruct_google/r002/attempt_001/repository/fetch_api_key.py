from security_client import access_secret
from security_models import SecretRef


def fetch_api_key(project_id: str, secret_id: str, version: str = "latest") -> str:
    return access_secret(SecretRef(project_id=project_id, secret_id=secret_id, version=version))
