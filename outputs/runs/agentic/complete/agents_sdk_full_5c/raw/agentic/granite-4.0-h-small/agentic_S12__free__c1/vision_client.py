import os
from typing import Any, Dict

def load_credentials() -> Dict[str, str]:
    """Load Google Cloud credentials from environment variable."""
    # The service account JSON can be set via GOOGLE_APPLICATION_CREDENTIALS
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_path:
        raise RuntimeError('Missing GOOGLE_APPLICATION_CREDENTIALS env var')
    return {'service_account_file': creds_path}

# Provide a simple wrapper around the Google Cloud client with the credentials

def get_client(service: str = 'vision') -> Any:
    """Instantiate and return a Google Cloud client for the given service."""
    from google.cloud import vision  # provider-specific import
    creds = load_credentials()
    # The client constructor looks for GOOGLE_APPLICATION_CREDENTIALS automatically,
    # but we also pass explicit credentials for clarity.
    return vision.ImageAnnotatorClient()
