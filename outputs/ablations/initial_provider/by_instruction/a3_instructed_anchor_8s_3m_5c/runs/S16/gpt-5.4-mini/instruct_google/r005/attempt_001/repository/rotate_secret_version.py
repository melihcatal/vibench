import os

from security_client import get_google_secret_manager_client, google_project_id, google_secret_name
from security_models import SecretResponse, normalize_secret_value


def rotate_secret_version(secret_id: str = None, version: str = None) -> SecretResponse:
    client = get_google_secret_manager_client()
    project_id = google_project_id()
    secret_id = secret_id or os.environ.get("GOOGLE_ROTATE_SECRET_ID", "rotating-secret")
    version = version or os.environ.get("GOOGLE_SECRET_VERSION", "latest")
    name = f"{google_secret_name(secret_id, project_id)}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return SecretResponse(provider="google-secret-manager", secret_id=secret_id, value=normalize_secret_value(response.payload.data), version=response.name)
