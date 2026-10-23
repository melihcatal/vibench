# helper file: security_client.py
from google.cloud import secretmanager

def get_gcp_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    """
    Initializes and returns a Google Cloud Secret Manager client.
    
    Authentication is handled automatically via Application Default Credentials.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        return client
    except Exception as e:
        print(f"Failed to create Secret Manager client: {e}")
        raise

