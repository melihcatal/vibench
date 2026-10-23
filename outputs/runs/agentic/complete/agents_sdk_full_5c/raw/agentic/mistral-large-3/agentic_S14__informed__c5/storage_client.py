from google.cloud import storage
import os
from typing import Optional

_storage_client: Optional[storage.Client] = None

def get_storage_client() -> storage.Client:
    """Initialize and return a Google Cloud Storage client."""
    global _storage_client
    if _storage_client is None:
        _storage_client = storage.Client()
    return _storage_client

def configure_storage_client(credentials_path: Optional[str] = None):
    """Configure the Google Cloud Storage client with optional credentials."""
    global _storage_client
    if credentials_path:
        _storage_client = storage.Client.from_service_account_json(credentials_path)
    else:
        _storage_client = storage.Client()