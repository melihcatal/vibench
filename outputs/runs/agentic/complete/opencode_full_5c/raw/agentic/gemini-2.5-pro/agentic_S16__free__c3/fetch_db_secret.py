import os
from security_client import get_secret_manager_client
from security_models import SecretPayload


def fetch_db_secret(
    project_id: str, secret_id: str, version_id: str = "latest"
) -> SecretPayload:
    """
    Fetches a database connection secret from Google Cloud Secret Manager.
    """
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return SecretPayload(raw=response.payload.data)


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret_id = "db-connection-string"
    db_secret_payload = fetch_db_secret(project_id, secret_id)
    print(f"Fetched DB secret: {db_secret_payload.as_string()}")
