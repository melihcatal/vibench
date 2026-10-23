from google.cloud import secretmanager

def get_secret_manager_client():
    """
    Provides a Google Cloud Secret Manager client.
    """\n    return secretmanager.SecretManagerServiceClient()

def build_secret_name(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Builds the full resource name for a secret version.
    """
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
