from google.cloud import secretmanager

def get_secret_manager_client():
    return secretmanager.SecretManagerServiceClient()

def get_secret_path(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
