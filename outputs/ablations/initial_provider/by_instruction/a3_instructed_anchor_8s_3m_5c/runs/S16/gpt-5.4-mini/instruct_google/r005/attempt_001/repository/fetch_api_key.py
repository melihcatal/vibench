import os

from google.cloud import secretmanager

from security_client import get_google_secret_manager_client, google_project_id, google_secret_name
from security_models import SecretResponse, normalize_secret_value


def fetch_api_key(secret_id: str = None) -> SecretResponse:
    client = get_google_secret_manager_client()
    project_id = google_project_id()
    secret_id = secret_id or os.environ.get("GOOGLE_API_KEY_SECRET_ID", "api-key")
    name = f"{google_secret_name(secret_id, project_id)}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    value = normalize_secret_value(response.payload.data)
    return SecretResponse(provider="google-secret-manager", secret_id=secret_id, value=value, version=response.name)
