import os
from security_client import get_secret_manager_client, build_secret_name
from security_models import SecretPayload


def fetch_api_key(project_id: str, secret_id: str) -> str:
    client = get_secret_manager_client()
    payload = SecretPayload(project_id=project_id, secret_id=secret_id)
    name = build_secret_name(payload)

    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
