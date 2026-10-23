from google.cloud import secretmanager

def get_secret_manager_client():
    """Returns a Google Secret Manager client."""
    return secretmanager.SecretManagerServiceClient()
