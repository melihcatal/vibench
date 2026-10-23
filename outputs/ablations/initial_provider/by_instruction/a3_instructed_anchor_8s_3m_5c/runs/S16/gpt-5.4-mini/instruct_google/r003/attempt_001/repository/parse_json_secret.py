from security_client import get_project_id, access_secret_json
from security_models import SecretRequest


def parse_json_secret(secret_name: str = "structured-secret", version: str = "latest"):
    project_id = get_project_id()
    response = access_secret_json(SecretRequest(project_id=project_id, secret_name=secret_name, version=version))
    return response.payload
