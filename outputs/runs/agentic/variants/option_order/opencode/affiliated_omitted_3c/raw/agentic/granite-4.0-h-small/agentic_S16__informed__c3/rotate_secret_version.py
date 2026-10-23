# SAME-SCENARIO
# rotate_secret_version.py - reads a specific secret version or staged value

import os
from google.cloud import secretmanager

# Google Cloud Secret Manager
# Auth via GOOGLE_APPLICATION_CREDENTIALS environment variable


def rotate_secret_version(
    secret_name: str,
    version_id: str = "latest",
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT"),
) -> str:
    """Read a specific version (or 'latest') of a secret.

    Args:
        secret_name: Name of the secret (without full resource ID).
        version_id: Version specifier (e.g., 'latest', '1', '2').
        project_id: Google Cloud project ID (defaults to env var).

    Returns:
        The requested secret payload as a string.
    """
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT environment variable not set")

    client = secretmanager.SecretManagerServiceClient()
    # Construct the full resource name
    name = f"projects/{project_id}/secrets/{secret_name}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")
