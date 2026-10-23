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
            raise ValueError(
                "Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable"
            )

    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(request={"name": secret_name})
        secret_data = response.payload.data.decode("UTF-8")

        # Parse as JSON for structured database secrets
        db_config = json.loads(secret_data)

        # Validate required fields
        required_fields = ["host", "port", "database", "username", "password"]
        for field in required_fields:
            if field not in db_config:
                raise ValueError(f"Missing required field in database secret: {field}")

        return db_config

    except Exception as e:
        if "NOT_FOUND" in str(e):
            raise ValueError(
                f"Secret {secret_id} not found in project {project_id}"
            ) from e
        elif "PERMISSION_DENIED" in str(e):
            raise PermissionError(
                f"Permission denied accessing secret {secret_id}"
            ) from e
        else:
            raise RuntimeError(f"Error fetching database secret: {e}") from e
