# storage_client.py
# [HELPER] Centralized configuration and client utilities for Managed Object Storage

import os
from google.cloud import storage


class ManagedStorageClient:
    """Helper class that provides a configured storage client.

    Loads credentials from environment or default Application Default Credentials.
    """

    _client = None

    @classmethod
    def get_client(cls) -> storage.Client:
        """Return a singleton Google Cloud Storage client.

        The client is lazily initialized, ensuring credentials are loaded only once.
        """
        if cls._client is None:
            # Use Application Default Credentials or explicit key file if set
            credentials = None
            credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if credential_path:
                from google.auth import credentials as ga_credentials

                credentials = ga_credentials.Credentials.from_service_account_file(
                    credential_path
                )
            cls._client = storage.Client(credentials=credentials)
        return cls._client
