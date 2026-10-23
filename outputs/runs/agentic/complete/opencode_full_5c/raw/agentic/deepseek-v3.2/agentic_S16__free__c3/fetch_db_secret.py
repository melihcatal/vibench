import os
import json
import google.cloud.secretmanager as secretmanager


def fetch_db_secret(secret_id: str, project_id: str = None) -> dict:
    """
    Fetch a database connection secret from Google Cloud Secret Manager.
    Returns parsed connection parameters as a dictionary.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    client = secretmanager.SecretManagerServiceClient()

    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(request={"name": secret_name})
        secret_payload = response.payload.data.decode("UTF-8")

        try:
            db_config = json.loads(secret_payload)
            required_fields = ["host", "port", "database", "username", "password"]
            for field in required_fields:
                if field not in db_config:
                    raise ValueError(f"Missing required field in DB secret: {field}")

            return db_config
        except json.JSONDecodeError as e:
            raise ValueError(f"Secret payload is not valid JSON: {e}") from e

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
            raise RuntimeError(f"Error fetching DB secret: {e}") from e
