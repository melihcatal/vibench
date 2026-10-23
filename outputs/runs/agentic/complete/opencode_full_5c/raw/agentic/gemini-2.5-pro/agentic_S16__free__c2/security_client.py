from google.cloud import secretmanager


def get_secret_manager_client():
    """Initializes and returns a Secret Manager client."""
    return secretmanager.SecretManagerServiceClient()
