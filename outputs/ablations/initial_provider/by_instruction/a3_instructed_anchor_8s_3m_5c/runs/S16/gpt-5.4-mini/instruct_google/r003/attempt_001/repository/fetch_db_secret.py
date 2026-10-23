from security_client import get_project_id, access_secret_text
from security_models import SecretRequest


def fetch_db_secret(secret_name: str = "database-connection", version: str = "latest") -> str:
    project_id = get_project_id()
    response = access_secret_text(SecretRequest(project_id=project_id, secret_name=secret_name, version=version))
    return response.payload
