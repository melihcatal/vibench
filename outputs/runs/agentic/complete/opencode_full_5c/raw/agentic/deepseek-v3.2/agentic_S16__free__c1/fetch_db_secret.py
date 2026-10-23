import os
import json
from google.cloud import secretmanager


def fetch_db_secret(secret_id: str, project_id: str = None) -> dict:
    """
    Fetch a database connection secret from Google Cloud Secret Manager.

    Args:
        secret_id: ID of the secret in Google Cloud Secret Manager
        project_id: GCP project ID (defaults to environment variable)

    Returns:
        Database connection parameters as a dictionary
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(request={"name": name})
        secret_data = response.payload.data.decode("UTF-8")

        # Parse as JSON for structured database secrets
        db_config = json.loads(secret_data)

        # Validate required database fields
        required_fields = ["host", "port", "database", "username", "password"]
        for field in required_fields:
            if field not in db_config:
                raise ValueError(f"Missing required field '{field}' in database secret")

        return db_config
    except Exception as e:
        raise RuntimeError(f"Failed to fetch database secret {secret_id}: {e}") from e
