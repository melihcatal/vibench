import os
from google.cloud import secretmanager


def fetch_db_secret(secret_name: str) -> dict:
    """Fetch a database connection secret from Google Cloud Secret Manager.
    Args:
        secret_name: The fully qualified secret ID (e.g., projects/123456/secrets/db-creds/versions/latest).
    Returns:
        A dict containing the secret payload (e.g., {\"username\": \"user\", \"password\": \"pwd\"}).
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS"
    )
    client = secretmanager.SecretManagerServiceClient()
    # Strip version if present and use latest
    if "/versions/" in secret_name:
        secret_name = secret_name.split("/versions/")[0] + "/versions/latest"
    response = client.access_secret_version(name=secret_name)
    payload = response.payload.data.decode("UTF-8")
    import json

    return json.loads(payload)
