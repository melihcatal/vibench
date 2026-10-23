import os

from security_client import get_google_secret_manager_client, google_project_id, google_secret_name
from security_models import SecretResponse, normalize_secret_value


def fetch_db_secret(secret_id: str = None) -> SecretResponse:
    client = get_google_secret_manager_client()
    project_id = google_project_id()
    secret_id = secret_id or os.environ.get("GOOGLE_DB_SECRET_ID", "db-secret")
    name = f"{google_secret_name(secret_id, project_id)}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return SecretResponse(provider="google-secret-manager", secret_id=secret_id, value=normalize_secret_value(response.payload.data), version=response.name)
