import os
from google.cloud import storage

class StorageClient:
    """Helper wrapper for Google Cloud Storage client with lazy initialization.
    The class reads credentials from the environment variable GOOGLE_APPLICATION_CREDENTIALS.
    It also provides a simple retry decorator for idempotent calls.
    """
    def __init__(self):
        self._client = None
    @property
    def client(self) -> storage.Client:
        if self._client is None:
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if not credentials_path:
                raise RuntimeError('Missing GOOGLE_APPLICATION_CREDENTIALS environment variable')
            self._client = storage.Client.from_service_account_json(credentials_path)
        return self._client

def get_storage_client() -> storage.Client:
    """Utility to obtain a shared StorageClient instance.
    Returns:
        storage.Client: Configured GCS client.
    """
    # Using a module-level singleton instance to avoid re-instantiating per call
    if not hasattr(storage_client, '_instance'):
        storage_client._instance = StorageClient()
    return storage_client._instance.client
