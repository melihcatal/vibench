from google.cloud import secretmanager


def get_secret_manager_client():
    """
    Creates and returns a client for Google Cloud Secret Manager.
    """
    return secretmanager.SecretManagerServiceClient()
