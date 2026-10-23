import os
from google.cloud import secretmanager

def get_secret_manager_client():
    """
    Initialize and return a Google Cloud Secret Manager client.
    """
    return secretmanager.SecretManagerServiceClient()