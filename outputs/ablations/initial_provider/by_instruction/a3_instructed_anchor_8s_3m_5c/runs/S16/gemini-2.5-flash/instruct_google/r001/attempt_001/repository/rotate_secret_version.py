from security_client import get_secret_manager_client
from security_models import SecretPayload

def rotate_secret_version(project_id: str, secret_id: str, version_id: str) -> SecretPayload:
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    secret_data = response.payload.data.decode("UTF-8")
    return SecretPayload(name=secret_id, data=secret_data, version=version_id)
